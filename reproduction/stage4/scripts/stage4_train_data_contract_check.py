#!/usr/bin/env python3
"""Stage 4B training-data contract check."""

import argparse
import os
from pathlib import Path
from typing import Any

import numpy as np


REQUIRED_KEYS = [
    "points",
    "images",
    "gt_boxes",
    "gt_boxes2d",
    "image_shape",
    "trans_lidar_to_cam",
    "trans_cam_to_img",
    "lidar_aug_matrix",
    "frame_id",
    "batch_size",
]


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


def describe_value(value: Any) -> str:
    if isinstance(value, np.ndarray):
        return f"ndarray shape={value.shape} dtype={value.dtype}"
    if hasattr(value, "shape") and hasattr(value, "dtype"):
        return f"{type(value).__name__} shape={tuple(value.shape)} dtype={value.dtype}"
    if isinstance(value, list):
        return f"list len={len(value)}"
    if isinstance(value, tuple):
        return f"tuple len={len(value)}"
    return f"{type(value).__name__} value={value}"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", required=True, choices=("vod", "tj4d"))
    parser.add_argument("--batch-size", type=int, default=1)
    parser.add_argument("--workers", type=int, default=0)
    parser.add_argument("--max-batches", type=int, default=2)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.max_batches <= 0:
        raise ValueError("--max-batches must be > 0")

    repo_root = resolve_repo_root()
    os.chdir(repo_root)

    from pcdet.config import cfg, cfg_from_yaml_file
    from pcdet.datasets import build_dataloader
    from pcdet.utils import common_utils

    cfg_path = {
        "vod": repo_root / "tools/cfgs/hgsfusion/hgsfusion_vod.yaml",
        "tj4d": repo_root / "tools/cfgs/hgsfusion/hgsfusion_tj4d.yaml",
    }[args.dataset]

    cfg_from_yaml_file(str(cfg_path), cfg)
    logger = common_utils.create_logger()

    dataset, dataloader, _ = build_dataloader(
        dataset_cfg=cfg.DATA_CONFIG,
        class_names=cfg.CLASS_NAMES,
        batch_size=args.batch_size,
        dist=False,
        workers=args.workers,
        logger=logger,
        training=True,
    )

    split_name = cfg.DATA_CONFIG.DATA_SPLIT["train"]
    info_list = list(cfg.DATA_CONFIG.INFO_PATH["train"])
    resolved_info_paths = [dataset.root_path / x for x in info_list]
    missing_info = [str(p) for p in resolved_info_paths if not p.exists()]

    virtual_prefix = cfg.DATA_CONFIG.get("VIRTUAL_POINT_PREFIX", "mask")
    hybrid_dir = dataset.root_path / "training" / virtual_prefix

    print(f"repo_root: {repo_root}")
    print(f"dataset: {args.dataset}")
    print(f"cfg_path: {cfg_path}")
    print(f"dataset_len: {len(dataset)}")
    print(f"resolved_dataset_root: {dataset.root_path}")
    print(f"train_data_split: {split_name}")
    print(f"train_info_path_cfg: {info_list}")
    for p in resolved_info_paths:
        print(f"train_info_path_resolved: {p} exists={p.exists()}")
    print(f"official_hybrid_point_dir: {hybrid_dir} exists={hybrid_dir.exists()}")

    if missing_info:
        raise FileNotFoundError(f"missing train info pkl: {missing_info}")
    if not hybrid_dir.exists():
        raise FileNotFoundError(f"missing official hybrid point dir: {hybrid_dir}")

    batch_iter = iter(dataloader)
    checked = 0
    for i in range(args.max_batches):
        batch = next(batch_iter)
        checked += 1
        keys = sorted(batch.keys())
        print(f"batch[{i}] keys({len(keys)}): {keys}")
        for key in REQUIRED_KEYS:
            if key not in batch:
                raise KeyError(f"missing required training key: {key}")
            print(f"batch[{i}] {key}: {describe_value(batch[key])}")

    print(f"TRAIN_DATA_CONTRACT_OK dataset={args.dataset} batches_checked={checked}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
