#!/usr/bin/env python3
import argparse
import os
from pathlib import Path

import torch


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


def cfg_path_for_dataset(repo_root: Path, dataset: str) -> Path:
    return {
        "vod": repo_root / "tools/cfgs/hgsfusion/hgsfusion_vod.yaml",
        "tj4d": repo_root / "tools/cfgs/hgsfusion/hgsfusion_tj4d.yaml",
    }[dataset]


def ckpt_path_for_dataset(dataset: str) -> Path:
    return Path(f"/home/user/HGSFusion_research/checkpoints/hgsfusion_{dataset}.pth")


def summarize_tensor(name, tensor):
    shape = tuple(tensor.shape) if hasattr(tensor, "shape") else "n/a"
    dtype = getattr(tensor, "dtype", "n/a")
    print(f"  - {name}: shape={shape}, dtype={dtype}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Stage 1 single-batch forward")
    parser.add_argument("--dataset", choices=["vod", "tj4d"], required=True)
    parser.add_argument("--ckpt", type=str, default=None)
    parser.add_argument("--batch-size", type=int, default=1)
    parser.add_argument("--workers", type=int, default=0)
    args = parser.parse_args()

    repo_root = resolve_repo_root()
    os.chdir(repo_root)

    cfg_path = cfg_path_for_dataset(repo_root, args.dataset)
    ckpt_path = Path(args.ckpt) if args.ckpt else ckpt_path_for_dataset(args.dataset)

    print(f"[INFO] repo root: {repo_root}")
    print(f"[INFO] dataset: {args.dataset}")
    print(f"[INFO] cfg path: {cfg_path}")
    print(f"[INFO] ckpt path: {ckpt_path.resolve()}")
    print(f"[INFO] batch_size={args.batch_size}, workers={args.workers}")

    from pcdet.config import cfg, cfg_from_yaml_file
    from pcdet.datasets import build_dataloader
    from pcdet.models import build_network, load_data_to_gpu
    from pcdet.utils import common_utils

    cfg_from_yaml_file(str(cfg_path), cfg)
    logger = common_utils.create_logger()

    dataset, dataloader, _ = build_dataloader(
        dataset_cfg=cfg.DATA_CONFIG,
        class_names=cfg.CLASS_NAMES,
        batch_size=args.batch_size,
        dist=False,
        workers=args.workers,
        logger=logger,
        training=False,
    )

    model = build_network(model_cfg=cfg.MODEL, num_class=len(cfg.CLASS_NAMES), dataset=dataset)
    model.load_params_from_file(filename=str(ckpt_path), logger=logger, to_cpu=False)

    model.cuda()
    model.eval()

    with torch.no_grad():
        batch = next(iter(dataloader))
        load_data_to_gpu(batch)
        pred_dicts, recall_dict = model(batch)

    print(f"[OK] pred_dicts type: {type(pred_dicts).__name__}")
    print(f"[OK] len(pred_dicts): {len(pred_dicts)}")
    if len(pred_dicts) > 0:
        keys = list(pred_dicts[0].keys())
        print(f"[OK] pred_dict keys: {keys}")
        for key in ["pred_boxes", "pred_scores", "pred_labels"]:
            if key in pred_dicts[0]:
                summarize_tensor(key, pred_dicts[0][key])
            else:
                print(f"  - {key}: missing")

    print(f"[OK] recall_dict keys: {list(recall_dict.keys())}")
    print("[OK] single-batch forward passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
