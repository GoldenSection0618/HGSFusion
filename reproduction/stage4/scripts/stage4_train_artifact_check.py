#!/usr/bin/env python3
"""Check train-after-eval artifacts for Stage 4."""

import argparse
import pickle
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--eval-output-dir", required=True)
    parser.add_argument("--expected-count", required=True, type=int)
    return parser.parse_args()


def find_eval_log(eval_output_dir: Path):
    logs = sorted(eval_output_dir.rglob("log_eval_*.txt"), key=lambda p: p.stat().st_mtime)
    if logs:
        return logs[-1]
    parent_chain = list(eval_output_dir.parents)
    roots = [eval_output_dir] + parent_chain[:4]
    merged = []
    for root in roots:
        merged.extend(root.glob("log_eval_*.txt"))
    merged = sorted(set(merged), key=lambda p: p.stat().st_mtime)
    if merged:
        return merged[-1]

    # train.py may emit eval markers directly into train_*.log.
    train_logs = []
    for root in roots:
        train_logs.extend(root.glob("train_*.log"))
    train_logs = sorted(set(train_logs), key=lambda p: p.stat().st_mtime)
    return train_logs[-1] if train_logs else None


def main() -> int:
    args = parse_args()
    eval_dir = Path(args.eval_output_dir).resolve()
    if not eval_dir.exists():
        raise FileNotFoundError(f"eval output dir not found: {eval_dir}")

    result_pkl = eval_dir / "result.pkl"
    if not result_pkl.exists():
        raise FileNotFoundError(f"result.pkl not found: {result_pkl}")
    with result_pkl.open("rb") as f:
        result_obj = pickle.load(f)
    if not isinstance(result_obj, list):
        raise TypeError(f"result.pkl must contain a list, got {type(result_obj).__name__}")
    actual_count = len(result_obj)
    if actual_count != args.expected_count:
        raise ValueError(
            f"result.pkl length mismatch: expected={args.expected_count}, actual={actual_count}"
        )

    pred_dir = eval_dir / "final_result" / "data"
    if not pred_dir.exists():
        raise FileNotFoundError(f"final_result/data not found: {pred_dir}")
    txt_count = len(list(pred_dir.glob("*.txt")))
    if txt_count != args.expected_count:
        raise ValueError(
            f"prediction txt count mismatch: expected={args.expected_count}, actual={txt_count}"
        )

    eval_log = find_eval_log(eval_dir)
    if eval_log is None:
        raise FileNotFoundError("eval log not found (log_eval_*.txt)")
    text = eval_log.read_text(encoding="utf-8", errors="ignore")
    if "Result is saved" not in text:
        raise ValueError("eval log missing marker: Result is saved")
    if "Evaluation done" not in text:
        raise ValueError("eval log missing marker: Evaluation done")

    print(f"eval_output_dir: {eval_dir}")
    print(f"result_pkl: {result_pkl}")
    print(f"result_count: {actual_count}")
    print(f"prediction_txt_count: {txt_count}")
    print(f"eval_log: {eval_log}")
    print(f"TRAIN_AFTER_EVAL_ARTIFACT_CHECK_OK expected={args.expected_count} actual={actual_count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
