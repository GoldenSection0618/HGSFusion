#!/usr/bin/env python3
"""Parse Stage 3 evaluation logs into JSON and summary CSV."""

import argparse
import csv
import json
from pathlib import Path
import re
import sys

VOD_SECTIONS = ["Entire annotated area:", "Driving corridor area:"]
TJ4D_WEATHERS = ["dark", "standard", "shiny", "all_weather"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", required=True, choices=("vod", "tj4d"))
    parser.add_argument("--eval-dir", required=True)
    parser.add_argument("--out-json", required=True)
    parser.add_argument("--out-csv", required=True)
    return parser.parse_args()


def find_log_files(eval_dir: Path):
    roots = [eval_dir]
    cur = eval_dir
    for _ in range(4):
        cur = cur.parent
        roots.append(cur)

    seen = set()
    logs = []
    for root in roots:
        root = root.resolve()
        if root in seen or not root.exists() or not root.is_dir():
            continue
        seen.add(root)
        logs.extend(root.glob("log_eval_*.txt"))

    return sorted(set(logs), key=lambda p: p.stat().st_mtime)


def clean_line(line: str) -> str:
    return line.strip()


def find_section_line_idx(lines, token: str):
    for idx, line in enumerate(lines):
        if token in line:
            return idx
    return -1


def parse_vod(lines, parser_notes):
    metrics = {}
    raw_lines = []

    key_value_re = re.compile(
        r"^(Car|Pedestrian|Cyclist|mAP)\s*:\s*([+-]?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?)\s*$"
    )

    for section in VOD_SECTIONS:
        start = find_section_line_idx(lines, section)
        if start < 0:
            parser_notes.append(f"missing section marker: {section}")
            continue

        if section == "Entire annotated area:":
            end = find_section_line_idx(lines[start + 1 :], "Driving corridor area:")
            end = start + 1 + end if end >= 0 else len(lines)
        else:
            end = len(lines)
            for idx in range(start + 1, len(lines)):
                if "Result is saved" in lines[idx] or "Evaluation done" in lines[idx]:
                    end = idx
                    break

        block = lines[start:end]
        raw_lines.extend(block)

        section_name = section.rstrip(":")
        section_metrics = {}
        for line in block[1:]:
            stripped = clean_line(line)
            match = key_value_re.match(stripped)
            if match:
                section_metrics[match.group(1)] = float(match.group(2))

        if section_metrics:
            metrics[section_name] = section_metrics
        else:
            parser_notes.append(f"section has no parseable numeric metrics: {section_name}")

    return metrics, raw_lines


def parse_tj4d(lines, parser_notes):
    metrics = {}
    raw_lines = []

    weather_positions = {}
    for weather in TJ4D_WEATHERS:
        token = f"Evaluating {weather}"
        idx = find_section_line_idx(lines, token)
        if idx >= 0:
            weather_positions[weather] = idx
        else:
            parser_notes.append(f"missing weather section marker: {token}")

    if not weather_positions:
        return metrics, raw_lines

    ordered = sorted(weather_positions.items(), key=lambda x: x[1])
    overall_re = re.compile(r"^Overall AP40@")
    class_re = re.compile(r"^(Pedestrian|Cyclist|Car|Truck)\s+AP40@(.+):$")
    metric_re = re.compile(r"^(bbox|bev|3d|aos)\s+AP:\s*([0-9.,\s]+)$")

    for i, (weather, start) in enumerate(ordered):
        end = ordered[i + 1][1] if i + 1 < len(ordered) else len(lines)
        for idx in range(start + 1, end):
            if "Result is saved" in lines[idx] or "Evaluation done" in lines[idx]:
                end = idx
                break

        block = lines[start:end]
        raw_lines.extend(block)

        weather_metrics = {}
        current_class = None
        current_thresh = None

        if any("No samples matched this weather subset." in x for x in block):
            weather_metrics["status"] = "no_samples"

        for line in block:
            stripped = clean_line(line)
            class_match = class_re.match(stripped)
            if class_match:
                current_class = class_match.group(1)
                current_thresh = class_match.group(2).strip()
                weather_metrics.setdefault("classes", {}).setdefault(current_class, {})
                weather_metrics["classes"][current_class].setdefault(current_thresh, {})
                continue

            metric_match = metric_re.match(stripped)
            if metric_match and current_class == "__overall__":
                values = [v.strip() for v in metric_match.group(2).split(",") if v.strip()]
                try:
                    parsed_values = [float(v) for v in values]
                except ValueError:
                    parser_notes.append(f"non-numeric overall AP line in {weather}: {stripped}")
                    continue
                weather_metrics.setdefault("overall", {})[metric_match.group(1)] = parsed_values
                continue

            if metric_match and current_class and current_thresh and current_class != "__overall__":
                values = [v.strip() for v in metric_match.group(2).split(",") if v.strip()]
                try:
                    parsed_values = [float(v) for v in values]
                except ValueError:
                    parser_notes.append(f"non-numeric AP line in {weather}: {stripped}")
                    continue
                weather_metrics["classes"][current_class][current_thresh][
                    metric_match.group(1)
                ] = parsed_values
                continue

            if overall_re.match(stripped):
                weather_metrics.setdefault("overall", {})
                current_class = "__overall__"
                current_thresh = "easy_moderate_hard"
                continue

        metrics[weather] = weather_metrics

    return metrics, raw_lines


def write_summary_csv(out_csv: Path, row: dict):
    fieldnames = [
        "dataset",
        "eval_dir",
        "log_file",
        "split_context",
        "status",
        "metrics_keys",
        "parser_notes_count",
    ]

    rows = []
    if out_csv.exists() and out_csv.is_file():
        with out_csv.open("r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            for r in reader:
                if r.get("dataset") == row["dataset"] and r.get("eval_dir") == row["eval_dir"]:
                    continue
                rows.append(r)

    rows.append(row)

    out_csv.parent.mkdir(parents=True, exist_ok=True)
    with out_csv.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    args = parse_args()

    eval_dir = Path(args.eval_dir)
    out_json = Path(args.out_json)
    out_csv = Path(args.out_csv)

    if not eval_dir.exists() or not eval_dir.is_dir():
        print(f"ERROR: eval dir not found: {eval_dir}", file=sys.stderr)
        return 2

    logs = find_log_files(eval_dir)
    if not logs:
        print("ERROR: no log_eval_*.txt found in eval dir or nearby parents", file=sys.stderr)
        return 2

    log_file = logs[-1]
    text = log_file.read_text(encoding="utf-8", errors="ignore")
    lines = text.splitlines()

    parser_notes = []
    result = {
        "dataset": args.dataset,
        "eval_dir": str(eval_dir),
        "log_file": str(log_file),
        "split_context": "",
        "metrics": {},
        "parser_notes": parser_notes,
    }

    if args.dataset == "vod":
        result["split_context"] = "VoD official-checkpoint evaluation using val info split."
        metrics, raw_lines = parse_vod(lines, parser_notes)
        result["metrics"] = metrics
        result.setdefault("metrics", {})["raw_lines"] = raw_lines
        missing = [sec for sec in VOD_SECTIONS if sec not in text]
        if missing:
            parser_notes.append("required VoD sections absent: " + ", ".join(missing))
            status = "missing_required_sections"
            rc = 1
        else:
            status = "ok"
            rc = 0
    else:
        result[
            "split_context"
        ] = "TJ4D official eval split / test-val alias split (kitti_infos_val.pkl)."
        metrics, raw_lines = parse_tj4d(lines, parser_notes)
        result["metrics"] = metrics
        result.setdefault("metrics", {})["raw_lines"] = raw_lines
        missing = [f"Evaluating {w}" for w in TJ4D_WEATHERS if f"Evaluating {w}" not in text]
        if missing:
            parser_notes.append("required TJ4D weather sections absent: " + ", ".join(missing))
            status = "missing_required_sections"
            rc = 1
        else:
            status = "ok"
            rc = 0

    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    write_summary_csv(
        out_csv,
        {
            "dataset": args.dataset,
            "eval_dir": str(eval_dir),
            "log_file": str(log_file),
            "split_context": result["split_context"],
            "status": status,
            "metrics_keys": ";".join(sorted(k for k in result["metrics"].keys() if k != "raw_lines")),
            "parser_notes_count": str(len(parser_notes)),
        },
    )

    print(f"dataset: {args.dataset}")
    print(f"eval_dir: {eval_dir}")
    print(f"log_file: {log_file}")
    print(f"out_json: {out_json}")
    print(f"out_csv: {out_csv}")
    print(f"status: {status}")
    print(f"parser_notes_count: {len(parser_notes)}")

    return rc


if __name__ == "__main__":
    raise SystemExit(main())
