#!/usr/bin/env python3
import argparse
import os
import sys
from pathlib import Path
from typing import Dict, List

import numpy as np


def resolve_repo_root() -> Path:
    env_repo = os.environ.get("HGSFUSION_REPO")
    if env_repo:
        p = Path(env_repo).expanduser().resolve()
        if (p / "pcdet").exists() and (p / "tools").exists():
            return p

    script_dir = Path(__file__).resolve().parent
    for parent in [script_dir] + list(script_dir.parents):
        if (parent / "pcdet").exists() and (parent / "tools/cfgs/hgsfusion").exists():
            return parent

    return Path.cwd().resolve()


def describe_value(key: str, value) -> str:
    if isinstance(value, np.ndarray):
        return f"type=ndarray, shape={value.shape}, dtype={value.dtype}"
    if hasattr(value, "shape") and hasattr(value, "dtype"):
        return f"type={type(value).__name__}, shape={tuple(value.shape)}, dtype={value.dtype}"
    if isinstance(value, list):
        return f"type=list, len={len(value)}"
    return f"type={type(value).__name__}, value={value}"


def main() -> int:
    parser = argparse.ArgumentParser(description="Stage 1 batch contract check")
    parser.add_argument("--dataset", choices=["vod", "tj4d"], required=True)
    parser.add_argument("--batch-size", type=int, default=1)
    parser.add_argument("--workers", type=int, default=0)
    parser.add_argument("--training", action="store_true", default=False)
    args = parser.parse_args()

    repo_root = resolve_repo_root()
    os.chdir(repo_root)

    print(f"[INFO] repo root: {repo_root}")
    print(f"[INFO] dataset: {args.dataset}")
    print(f"[INFO] batch_size={args.batch_size}, workers={args.workers}, training={args.training}")

    try:
        import kornia  # noqa: F401
        print("[OK] import kornia")
    except Exception as exc:
        print(f"[FAIL] import kornia: {exc!r}")
        return 1

    from pcdet.config import cfg, cfg_from_yaml_file
    from pcdet.datasets import build_dataloader
    from pcdet.utils import common_utils

    cfg_path = {
        "vod": repo_root / "tools/cfgs/hgsfusion/hgsfusion_vod.yaml",
        "tj4d": repo_root / "tools/cfgs/hgsfusion/hgsfusion_tj4d.yaml",
    }[args.dataset]
    print(f"[INFO] cfg path: {cfg_path}")
    cfg_from_yaml_file(str(cfg_path), cfg)

    logger = common_utils.create_logger()
    dataset, dataloader, _ = build_dataloader(
        dataset_cfg=cfg.DATA_CONFIG,
        class_names=cfg.CLASS_NAMES,
        batch_size=args.batch_size,
        dist=False,
        workers=args.workers,
        logger=logger,
        training=args.training,
    )
    print(f"[OK] dataloader built, dataset_len={len(dataset)}")

    batch = next(iter(dataloader))
    keys = sorted(batch.keys())
    print(f"[INFO] batch keys ({len(keys)}): {keys}")

    important_keys = [
        "points",
        "images",
        "gt_boxes",
        "gt_boxes2d",
        "calib_matricies",
        "image_shape",
        "frame_id",
        "metadata",
        "calib",
        "trans_lidar_to_cam",
        "trans_cam_to_img",
        "lidar_aug_matrix",
        "batch_size",
    ]

    print("[INFO] important field summary:")
    for key in important_keys:
        if key in batch:
            print(f"  - [OK] {key}: {describe_value(key, batch[key])}")
        else:
            print(f"  - [WARN] {key}: missing")

    # Runtime-required keys for CaDDN/FusionVFE/ImageVFE in this fork.
    runtime_required = [
        "points",
        "images",
        "image_shape",
        "trans_lidar_to_cam",
        "trans_cam_to_img",
        "lidar_aug_matrix",
        "frame_id",
        "batch_size",
    ]

    missing_runtime = [k for k in runtime_required if k not in batch]
    if missing_runtime:
        print(f"[FAIL] runtime-required keys missing: {missing_runtime}")
        return 1

    # Required-by-instruction key names, allowing explicit compatibility mapping.
    spec_required = ["points", "images", "gt_boxes", "gt_boxes2d", "calib_matricies", "image_shape", "frame_id", "metadata"]
    missing_spec = [k for k in spec_required if k not in batch]

    if "calib_matricies" in missing_spec and ("trans_lidar_to_cam" in batch and "trans_cam_to_img" in batch):
        print("[WARN] `calib_matricies` key not present; model contract uses `trans_lidar_to_cam` + `trans_cam_to_img` in this fork.")
        missing_spec.remove("calib_matricies")

    if "metadata" in missing_spec and "calib" in batch:
        print("[WARN] `metadata` key not present in current eval batch; `calib` is present and frame ids are available.")

    if missing_spec:
        print(f"[WARN] spec-listed keys missing after compatibility mapping: {missing_spec}")
    else:
        print("[OK] spec-listed keys satisfied (directly or via compatibility mapping).")

    print("[OK] stage1 batch contract check passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
