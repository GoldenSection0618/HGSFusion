#!/usr/bin/env python3
"""Validate full-evaluation artifact contract for Stage 3."""

import argparse
from pathlib import Path
import pickle
import sys

REQUIRED_MARKERS = [
    "recall_roi",
    "recall_rcnn",
    "Average predicted number",
    "Result is saved",
    "Evaluation done",
]

DATASET_CONTEXT_MARKERS = {
    "vod": ["Entire annotated area", "Driving corridor area", "mAP"],
    "tj4d": ["Evaluating dark", "Evaluating standard", "Evaluating shiny", "Evaluating all_weather"],
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--info-pkl", required=True, help="Path to full info pkl list")
    parser.add_argument("--eval-dir", required=True, help="Path to eval output directory")
    parser.add_argument("--dataset", required=True, choices=("vod", "tj4d"), help="Dataset name")
    return parser.parse_args()


def load_pickle_list(path: Path, label: str):
    try:
        with path.open("rb") as f:
            obj = pickle.load(f)
    except Exception as exc:  # pragma: no cover
        raise ValueError(f"{label} is unreadable: {path} ({exc})") from exc

    if not isinstance(obj, list):
        raise ValueError(f"{label} is not a list: {path} (type={type(obj).__name__})")
    return obj


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

    unique_logs = sorted(set(logs), key=lambda p: p.stat().st_mtime)
    return unique_logs


def main() -> int:
    args = parse_args()

    info_pkl = Path(args.info_pkl)
    eval_dir = Path(args.eval_dir)

    if not info_pkl.exists():
        print(f"ERROR: info pkl not found: {info_pkl}", file=sys.stderr)
        return 2
    if not eval_dir.exists() or not eval_dir.is_dir():
        print(f"ERROR: eval dir not found: {eval_dir}", file=sys.stderr)
        return 2

    try:
        info_list = load_pickle_list(info_pkl, "info_pkl")
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    result_pkl = eval_dir / "result.pkl"
    if not result_pkl.exists():
        result_list = None
        result_load_error = None
    else:
        try:
            result_list = load_pickle_list(result_pkl, "result.pkl")
            result_load_error = None
        except ValueError as exc:
            result_list = None
            result_load_error = str(exc)

    final_data_dir = eval_dir / "final_result" / "data"
    final_data_exists = final_data_dir.exists() and final_data_dir.is_dir()
    txt_count = len(list(final_data_dir.glob("*.txt"))) if final_data_exists else 0

    log_candidates = find_log_files(eval_dir)
    chosen_log = log_candidates[-1] if log_candidates else None

    marker_hits = {m: False for m in REQUIRED_MARKERS}
    context_hits = {m: False for m in DATASET_CONTEXT_MARKERS[args.dataset]}

    if chosen_log is not None:
        text = chosen_log.read_text(encoding="utf-8", errors="ignore")
        for marker in marker_hits:
            marker_hits[marker] = marker in text
        for marker in context_hits:
            context_hits[marker] = marker in text

    info_count = len(info_list)
    result_exists = result_pkl.exists()
    result_count = len(result_list) if isinstance(result_list, list) else -1

    print(f"dataset: {args.dataset}")
    print(f"info_pkl: {info_pkl}")
    print(f"info_count: {info_count}")
    print(f"eval_dir: {eval_dir}")
    print(f"result_pkl_exists: {result_exists}")
    print(f"result_count: {result_count}")
    print(f"final_result_data_exists: {final_data_exists}")
    print(f"prediction_txt_count: {txt_count}")
    print(f"log_file: {chosen_log if chosen_log else '<not found>'}")
    for marker, hit in marker_hits.items():
        print(f"marker[{marker}]: {hit}")
    for marker, hit in context_hits.items():
        print(f"marker[{marker}]: {hit}")

    contract_failures = []

    if not result_exists:
        contract_failures.append("missing result.pkl")
    if result_load_error is not None:
        print(f"ERROR: {result_load_error}", file=sys.stderr)
        return 2
    if isinstance(result_list, list) and len(result_list) != info_count:
        contract_failures.append(
            f"result.pkl length mismatch (result={len(result_list)}, info={info_count})"
        )
    if not final_data_exists:
        contract_failures.append("missing final_result/data")
    if final_data_exists and txt_count != info_count:
        contract_failures.append(
            f"prediction txt count mismatch (txt={txt_count}, info={info_count})"
        )
    if chosen_log is None:
        contract_failures.append("missing log_eval_*.txt")
    else:
        missing_core = [m for m, hit in marker_hits.items() if not hit]
        missing_ctx = [m for m, hit in context_hits.items() if not hit]
        if missing_core:
            contract_failures.append("missing core log markers: " + ", ".join(missing_core))
        if missing_ctx:
            contract_failures.append(
                "missing dataset log markers: " + ", ".join(missing_ctx)
            )

    if contract_failures:
        print("contract_check: FAIL")
        for item in contract_failures:
            print(f"contract_failure: {item}")
        return 1

    print("contract_check: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
