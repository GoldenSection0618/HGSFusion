#!/usr/bin/env python3
"""Parse Stage 4 train/eval logs for bounded training-chain checks."""

import argparse
import math
import re
from pathlib import Path
from typing import List, Optional


LOSS_RE = re.compile(r"(?:Loss:|loss[:=])\s*([+-]?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?)")
EPOCH_RE = re.compile(r"Train:\s+(\d+)/(\d+)")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", default=None, help="Training output directory")
    parser.add_argument("--log-file", default=None, help="Explicit train log file path")
    return parser.parse_args()


def choose_train_log(output_dir: Path) -> Optional[Path]:
    logs = sorted(output_dir.glob("train_*.log"), key=lambda p: p.stat().st_mtime)
    return logs[-1] if logs else None


def choose_eval_logs(output_dir: Path) -> List[Path]:
    eval_root = output_dir / "eval"
    if not eval_root.exists():
        return []
    logs = sorted(eval_root.rglob("log_eval_*.txt"), key=lambda p: p.stat().st_mtime)
    return logs


def main() -> int:
    args = parse_args()
    if not args.output_dir and not args.log_file:
        raise ValueError("either --output-dir or --log-file is required")

    output_dir = Path(args.output_dir).resolve() if args.output_dir else None
    if output_dir and not output_dir.exists():
        raise FileNotFoundError(f"output dir not found: {output_dir}")

    if args.log_file:
        train_log = Path(args.log_file).resolve()
    else:
        train_log = choose_train_log(output_dir)
        if train_log is None:
            raise FileNotFoundError(f"no train_*.log found under {output_dir}")
    if not train_log.exists():
        raise FileNotFoundError(f"train log not found: {train_log}")

    text = train_log.read_text(encoding="utf-8", errors="ignore")
    lines = text.splitlines()

    train_started = "Start training" in text
    train_ended = "End training" in text
    eval_started = "Start evaluation" in text
    eval_ended = "End evaluation" in text
    has_error = ("Traceback (most recent call last):" in text) or ("ERROR" in text)

    observed_epochs = []
    loss_values = []
    nan_or_inf_loss = False
    for line in lines:
        m_epoch = EPOCH_RE.search(line)
        if m_epoch:
            observed_epochs.append(int(m_epoch.group(1)))
        for m_loss in LOSS_RE.finditer(line):
            v = float(m_loss.group(1))
            loss_values.append(v)
            if math.isnan(v) or math.isinf(v):
                nan_or_inf_loss = True

    epoch_count_observed = len(set(observed_epochs))

    ckpt_mentions = [
        ln for ln in lines if ("checkpoint_epoch_" in ln) or ("Save latest model to" in ln) or ("Loading parameters from checkpoint" in ln)
    ]

    eval_logs = choose_eval_logs(output_dir) if output_dir else []
    eval_log = eval_logs[-1] if eval_logs else None
    eval_text = eval_log.read_text(encoding="utf-8", errors="ignore") if eval_log else ""
    eval_has_saved = "Result is saved" in eval_text
    eval_has_done = "Evaluation done" in eval_text
    eval_has_error = ("Traceback (most recent call last):" in eval_text) or ("ERROR" in eval_text)

    print(f"train_log: {train_log}")
    print(f"output_dir: {output_dir if output_dir else '<unspecified>'}")
    print(f"train_started: {train_started}")
    print(f"train_ended: {train_ended}")
    print(f"epoch_count_observed: {epoch_count_observed}")
    print(f"loss_entry_count: {len(loss_values)}")
    if loss_values:
        print(f"loss_first: {loss_values[0]}")
        print(f"loss_last: {loss_values[-1]}")
    print(f"nan_or_inf_loss: {nan_or_inf_loss}")
    print(f"checkpoint_message_count: {len(ckpt_mentions)}")
    print(f"eval_started_marker_in_train_log: {eval_started}")
    print(f"eval_ended_marker_in_train_log: {eval_ended}")
    print(f"error_or_traceback_in_train_log: {has_error}")
    print(f"eval_log: {eval_log if eval_log else '<not found>'}")
    print(f"eval_log_result_saved: {eval_has_saved}")
    print(f"eval_log_evaluation_done: {eval_has_done}")
    print(f"error_or_traceback_in_eval_log: {eval_has_error}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
