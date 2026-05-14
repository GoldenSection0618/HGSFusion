#!/usr/bin/env python3
"""Generate compact Stage 4 runtime summary JSON/CSV."""

import argparse
import csv
import json
import re
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-root",
        default="output/stage4/local_cfgs",
        help="Root of Stage 4 training outputs",
    )
    parser.add_argument(
        "--out-json",
        default="reproduction/stage4/outputs/stage4_training_summary.json",
    )
    parser.add_argument(
        "--out-csv",
        default="reproduction/stage4/outputs/stage4_training_summary.csv",
    )
    return parser.parse_args()


def infer_mode(extra_tag: str) -> str:
    lower = extra_tag.lower()
    if "ddp" in lower:
        return "ddp_syncbn"
    if "resume" in lower:
        return "resume"
    if "tj4d" in lower:
        return "tj4d_single_gpu"
    return "single_gpu"


def parse_field(text: str, key: str):
    m = re.search(rf"^{re.escape(key)}\s+(.+)$", text, flags=re.MULTILINE)
    return m.group(1).strip() if m else None


def eval_artifact_status(run_dir: Path) -> str:
    eval_root = run_dir / "eval"
    if not eval_root.exists():
        return "skipped"
    result_pkls = list(eval_root.rglob("result.pkl"))
    if not result_pkls:
        return "fail"
    for rp in result_pkls:
        pred_dir = rp.parent / "final_result" / "data"
        if pred_dir.exists():
            return "pass"
    return "fail"


def summarize_run(run_dir: Path):
    train_logs = sorted(run_dir.glob("train_*.log"), key=lambda p: p.stat().st_mtime)
    log_path = train_logs[-1] if train_logs else None
    text = log_path.read_text(encoding="utf-8", errors="ignore") if log_path else ""
    cfg_files = list(run_dir.glob("*.yaml"))
    ckpts = list((run_dir / "ckpt").glob("checkpoint_epoch_*.pth")) if (run_dir / "ckpt").exists() else []

    runtime_seconds = None
    if log_path:
        runtime_seconds = max(0.0, log_path.stat().st_mtime - log_path.stat().st_ctime)

    extra_tag = run_dir.name
    status = "success" if "End training" in text else "incomplete"
    if "Traceback (most recent call last):" in text:
        status = "failed"

    return {
        "dataset": "tj4d" if "tj4d" in extra_tag.lower() else "vod",
        "mode": infer_mode(extra_tag),
        "cfg_file": str(cfg_files[0]) if cfg_files else "",
        "extra_tag": extra_tag,
        "epochs_requested": parse_field(text, "epochs") or "",
        "batch_size": parse_field(text, "batch_size") or "",
        "workers": parse_field(text, "workers") or "",
        "output_directory": str(run_dir),
        "checkpoint_created": "yes" if ckpts else "no",
        "eval_artifact_check": eval_artifact_status(run_dir),
        "approx_runtime_seconds": f"{runtime_seconds:.1f}" if runtime_seconds is not None else "",
        "final_status": status,
    }


def main() -> int:
    args = parse_args()
    output_root = Path(args.output_root).resolve()
    out_json = Path(args.out_json).resolve()
    out_csv = Path(args.out_csv).resolve()

    rows = []
    if output_root.exists():
        for cfg_dir in sorted([p for p in output_root.iterdir() if p.is_dir()]):
            for run_dir in sorted([p for p in cfg_dir.iterdir() if p.is_dir()]):
                rows.append(summarize_run(run_dir))

    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(rows, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    fieldnames = [
        "dataset",
        "mode",
        "cfg_file",
        "extra_tag",
        "epochs_requested",
        "batch_size",
        "workers",
        "output_directory",
        "checkpoint_created",
        "eval_artifact_check",
        "approx_runtime_seconds",
        "final_status",
    ]
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    with out_csv.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)

    print(f"output_root: {output_root}")
    print(f"run_count: {len(rows)}")
    print(f"out_json: {out_json}")
    print(f"out_csv: {out_csv}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
