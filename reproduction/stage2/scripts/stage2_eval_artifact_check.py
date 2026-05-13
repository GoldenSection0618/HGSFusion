#!/usr/bin/env python3
"""Validate Stage 2 evaluation artifacts under an eval output directory."""

import argparse
from pathlib import Path
import sys


REQUIRED_MARKERS = [
    "recall_roi",
    "recall_rcnn",
    "Average predicted number",
    "Result is saved",
    "Evaluation done",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--eval-dir", required=True, help="Directory that should contain result.pkl")
    return parser.parse_args()


def find_log_files(eval_dir: Path):
    parents = [eval_dir, eval_dir.parent, eval_dir.parent.parent]
    seen = set()
    files = []
    for root in parents:
        root = root.resolve()
        if root in seen or not root.exists() or not root.is_dir():
            continue
        seen.add(root)
        files.extend(root.glob("log_eval_*.txt"))
    return sorted(set(files), key=lambda p: p.stat().st_mtime)


def main() -> int:
    args = parse_args()
    eval_dir = Path(args.eval_dir)

    if not eval_dir.exists() or not eval_dir.is_dir():
        print(f"ERROR: eval dir not found: {eval_dir}", file=sys.stderr)
        return 2

    result_pkl = eval_dir / "result.pkl"
    final_data_dir = eval_dir / "final_result" / "data"

    has_result = result_pkl.exists()
    has_final_data = final_data_dir.exists() and final_data_dir.is_dir()
    txt_count = len(list(final_data_dir.glob("*.txt"))) if has_final_data else 0

    log_candidates = find_log_files(eval_dir)
    chosen_log = log_candidates[-1] if log_candidates else None

    marker_hits = {m: False for m in REQUIRED_MARKERS}
    if chosen_log is not None:
        text = chosen_log.read_text(encoding="utf-8", errors="ignore")
        for marker in REQUIRED_MARKERS:
            marker_hits[marker] = marker in text

    print(f"eval_dir: {eval_dir}")
    print(f"result_pkl_exists: {has_result}")
    print(f"final_result_data_exists: {has_final_data}")
    print(f"prediction_txt_count: {txt_count}")
    print(f"log_file: {chosen_log if chosen_log else '<not found>'}")
    for marker, hit in marker_hits.items():
        print(f"marker[{marker}]: {hit}")

    missing = []
    if not has_result:
        missing.append("result.pkl")
    if not has_final_data:
        missing.append("final_result/data")
    if has_final_data and txt_count == 0:
        missing.append("prediction txt files")
    if chosen_log is None:
        missing.append("log_eval_*.txt")
    else:
        missing_markers = [m for m, hit in marker_hits.items() if not hit]
        if missing_markers:
            missing.append("log markers: " + ", ".join(missing_markers))

    if missing:
        print("ERROR: missing required artifacts/checks -> " + "; ".join(missing), file=sys.stderr)
        return 1

    print("artifact_check: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
