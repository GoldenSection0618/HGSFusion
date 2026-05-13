#!/usr/bin/env python3
import argparse
import os
from pathlib import Path
from typing import Dict, List, Tuple

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


def build_dataset_loader_model(repo_root: Path, cfg_path: Path):
    from pcdet.config import cfg, cfg_from_yaml_file
    from pcdet.datasets import build_dataloader
    from pcdet.models import build_network
    from pcdet.utils import common_utils

    cfg_from_yaml_file(str(cfg_path), cfg)
    logger = common_utils.create_logger()

    dataset, dataloader, _ = build_dataloader(
        dataset_cfg=cfg.DATA_CONFIG,
        class_names=cfg.CLASS_NAMES,
        batch_size=1,
        dist=False,
        workers=0,
        logger=logger,
        training=False,
    )
    model = build_network(model_cfg=cfg.MODEL, num_class=len(cfg.CLASS_NAMES), dataset=dataset)
    return cfg, dataset, dataloader, model


def resolve_deeplab_path(raw_path: str, repo_root: Path) -> Path:
    p = Path(raw_path)
    if p.is_absolute():
        return p
    # Runtime usually resolves relative to cwd (repo root in our commands)
    return (repo_root / p).resolve()


def compare_state_dicts(model_state: Dict[str, torch.Tensor], ckpt_state: Dict[str, torch.Tensor]):
    model_keys = set(model_state.keys())
    ckpt_keys = set(ckpt_state.keys())

    matched = model_keys & ckpt_keys
    missing = sorted(model_keys - ckpt_keys)
    unexpected = sorted(ckpt_keys - model_keys)

    shape_mismatch = []
    for key in sorted(matched):
        m_shape = tuple(model_state[key].shape)
        c_shape = tuple(ckpt_state[key].shape)
        if m_shape != c_shape:
            shape_mismatch.append((key, m_shape, c_shape))

    shape_mismatch_keys = {k for k, _, _ in shape_mismatch}
    exact_matched = len(matched) - len(shape_mismatch)

    return {
        "model_total": len(model_state),
        "ckpt_total": len(ckpt_state),
        "matched": len(matched),
        "exact_matched": exact_matched,
        "missing": missing,
        "unexpected": unexpected,
        "shape_mismatch": shape_mismatch,
    }


def print_build_info(cfg, model, repo_root: Path):
    print(f"[OK] model class: {model.__class__.__name__}")

    if hasattr(model, "module_topology"):
        print(f"[OK] module_topology: {list(model.module_topology)}")
    else:
        print("[WARN] module_topology not available on model")

    if hasattr(model, "module_list"):
        names = [m.__class__.__name__ for m in model.module_list]
        print(f"[OK] module_list classes ({len(names)}): {names}")
    else:
        print("[WARN] module_list not available on model")

    state = model.state_dict()
    print(f"[OK] len(model.state_dict()): {len(state)}")

    deeplab_raw = None
    try:
        deeplab_raw = cfg.MODEL.FusionVFE.ImageVFE.FFN.DDN.ARGS.pretrained_path
    except Exception:
        pass

    if deeplab_raw is None:
        print("[WARN] DeepLabV3 pretrained path not found in cfg at MODEL.FusionVFE.ImageVFE.FFN.DDN.ARGS.pretrained_path")
    else:
        resolved = resolve_deeplab_path(deeplab_raw, repo_root)
        print(f"[OK] deeplab raw path in cfg: {deeplab_raw}")
        print(f"[OK] deeplab resolved path: {resolved}")
        print(f"[OK] deeplab exists at build time: {resolved.exists()}")


def run_build_only(repo_root: Path, dataset: str) -> int:
    cfg_path = cfg_path_for_dataset(repo_root, dataset)
    print(f"[INFO] repo root: {repo_root}")
    print(f"[INFO] dataset: {dataset}")
    print(f"[INFO] cfg path: {cfg_path}")

    cfg, _, _, model = build_dataset_loader_model(repo_root, cfg_path)
    print_build_info(cfg, model, repo_root)
    print("[OK] build-only check passed")
    return 0


def run_audit(repo_root: Path, dataset: str, ckpt_path: Path) -> int:
    cfg_path = cfg_path_for_dataset(repo_root, dataset)
    print(f"[INFO] repo root: {repo_root}")
    print(f"[INFO] dataset: {dataset}")
    print(f"[INFO] cfg path: {cfg_path}")
    print(f"[INFO] checkpoint path: {ckpt_path.resolve()}")

    cfg, _, _, model = build_dataset_loader_model(repo_root, cfg_path)
    print_build_info(cfg, model, repo_root)

    checkpoint = torch.load(str(ckpt_path), map_location="cpu")
    if not isinstance(checkpoint, dict):
        print(f"[FAIL] checkpoint is not dict: type={type(checkpoint)}")
        return 1

    top_keys = list(checkpoint.keys())
    print(f"[OK] checkpoint top-level keys: {top_keys}")

    if "model_state" not in checkpoint:
        print("[FAIL] checkpoint missing required key: model_state")
        return 1

    ckpt_state = checkpoint["model_state"]
    model_state = model.state_dict()
    summary = compare_state_dicts(model_state=model_state, ckpt_state=ckpt_state)

    print(f"[OK] len(checkpoint['model_state']): {summary['ckpt_total']}")
    print(f"[OK] len(model.state_dict()): {summary['model_total']}")
    print(f"[OK] matched key count: {summary['matched']}")
    print(f"[OK] exact matched key count: {summary['exact_matched']}")
    print(f"[OK] missing key count: {len(summary['missing'])}")
    print(f"[OK] unexpected key count: {len(summary['unexpected'])}")
    print(f"[OK] shape mismatch key count: {len(summary['shape_mismatch'])}")

    ratio = 0.0
    if summary["model_total"] > 0:
        ratio = summary["exact_matched"] / summary["model_total"]
    print(f"[OK] matched ratio (exact/model_total): {ratio:.6f}")

    top_missing = summary["missing"][:20]
    top_unexpected = summary["unexpected"][:20]
    print(f"[INFO] top missing keys (up to 20): {top_missing}")
    print(f"[INFO] top unexpected keys (up to 20): {top_unexpected}")

    if summary["shape_mismatch"]:
        print("[INFO] all shape mismatch keys:")
        for key, m_shape, c_shape in summary["shape_mismatch"]:
            print(f"  - {key}: model{m_shape} vs ckpt{c_shape}")

    print("[OK] checkpoint audit completed")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Stage 1 checkpoint/model audit")
    parser.add_argument("--dataset", choices=["vod", "tj4d"], required=True)
    parser.add_argument("--mode", choices=["build-only", "audit"], required=True)
    parser.add_argument("--ckpt", type=str, default=None)
    args = parser.parse_args()

    repo_root = resolve_repo_root()
    os.chdir(repo_root)

    ckpt_path = Path(args.ckpt) if args.ckpt else ckpt_path_for_dataset(args.dataset)

    if args.mode == "build-only":
        return run_build_only(repo_root=repo_root, dataset=args.dataset)
    return run_audit(repo_root=repo_root, dataset=args.dataset, ckpt_path=ckpt_path)


if __name__ == "__main__":
    raise SystemExit(main())
