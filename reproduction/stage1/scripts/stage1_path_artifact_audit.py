#!/usr/bin/env python3
import argparse
import os
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Optional, Tuple


@dataclass
class CheckResult:
    status: str
    label: str
    path: Path
    size_bytes: Optional[int] = None
    note: str = ""


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


def file_size_bytes(path: Path) -> Optional[int]:
    try:
        return path.stat().st_size
    except OSError:
        return None


def format_size(num: Optional[int]) -> str:
    if num is None:
        return "n/a"
    units = ["B", "KB", "MB", "GB", "TB"]
    size = float(num)
    idx = 0
    while size >= 1024 and idx < len(units) - 1:
        size /= 1024.0
        idx += 1
    return f"{size:.2f}{units[idx]}"


def check_path(label: str, path: Path, required: bool, with_size: bool = False) -> Tuple[CheckResult, bool]:
    exists = path.exists()
    if exists:
        size = file_size_bytes(path) if with_size else None
        return CheckResult("OK", label, path.resolve(), size_bytes=size), True
    status = "MISSING" if required else "OPTIONAL-MISSING"
    return CheckResult(status, label, path.resolve(), size_bytes=None), (not required)


def pick_existing(candidates: Iterable[Path]) -> Optional[Path]:
    for c in candidates:
        if c.exists():
            return c
    return None


def discover_checkpoint(dataset: str, checkpoint_root: Path, repo_root: Path) -> Tuple[Optional[Path], str]:
    expected = checkpoint_root / f"hgsfusion_{dataset}.pth"
    if expected.exists():
        return expected, "expected"

    patterns = [
        f"hgsfusion_{dataset}.pth",
        f"hgsfusion_{dataset}*.pth",
        f"*{dataset}*.pth",
    ]

    for pattern in patterns:
        for p in sorted(checkpoint_root.glob(pattern)):
            if p.exists():
                return p, f"discovered in {checkpoint_root} via {pattern}"

    for root in [repo_root, repo_root.parent]:
        for pattern in patterns:
            for p in sorted(root.rglob(pattern)):
                if p.is_file() and "checkpoints" in p.parts:
                    return p, f"discovered outside checkpoint root via {pattern}"

    return None, "not found"


def build_checks(repo_root: Path, dataset: str) -> Tuple[List[Tuple[str, Path, bool, bool]], Path, Path]:
    data_root = repo_root / "data"
    checkpoint_root = Path("/home/user/HGSFusion_research/checkpoints")
    deeplab = checkpoint_root / "deeplabv3_resnet101_coco-586e9e4e.pth"

    if dataset == "vod":
        checks = [
            ("model config", repo_root / "tools/cfgs/hgsfusion/hgsfusion_vod.yaml", True, False),
            ("dataset config", repo_root / "tools/cfgs/dataset_configs/vod_fusion.yaml", True, False),
            ("dataset root", data_root / "vod_radar_5frames", True, False),
            ("dataset val info", data_root / "vod_radar_5frames/kitti_infos_val.pkl", True, False),
            (
                "official hybrid points dir",
                data_root / "vod_radar_5frames/training/mask_maskformer_with_label_k_1_gauss_k_4_uniform",
                True,
                False,
            ),
            ("deeplabv3 pretrained", deeplab, True, True),
        ]
    else:
        checks = [
            ("model config", repo_root / "tools/cfgs/hgsfusion/hgsfusion_tj4d.yaml", True, False),
            ("dataset config", repo_root / "tools/cfgs/dataset_configs/tj4d_fusion.yaml", True, False),
            ("dataset root", data_root / "tj4d", True, False),
            ("dataset val info", data_root / "tj4d/kitti_infos_val.pkl", True, False),
            (
                "official hybrid points dir",
                data_root / "tj4d/training/mask_maskformer_with_label_k_1_gauss_k_4_uniform",
                True,
                False,
            ),
            ("deeplabv3 pretrained", deeplab, True, True),
        ]

    return checks, checkpoint_root, deeplab


def main() -> int:
    parser = argparse.ArgumentParser(description="Stage 1 path/artifact audit")
    parser.add_argument("--dataset", choices=["vod", "tj4d"], required=True)
    args = parser.parse_args()

    repo_root = resolve_repo_root()
    checks, checkpoint_root, _ = build_checks(repo_root, args.dataset)

    print(f"[INFO] repo root: {repo_root}")
    print(f"[INFO] dataset: {args.dataset}")
    print(f"[INFO] checkpoint root: {checkpoint_root}")

    all_ok = True

    for label, path, required, with_size in checks:
        result, ok = check_path(label, path, required=required, with_size=with_size)
        suffix = f", size={format_size(result.size_bytes)}" if with_size else ""
        print(f"[{result.status}] {label}: {result.path}{suffix}")
        all_ok &= ok

    checkpoint, source_note = discover_checkpoint(args.dataset, checkpoint_root, repo_root)
    if checkpoint is None:
        missing_path = checkpoint_root / f"hgsfusion_{args.dataset}.pth"
        print(f"[MISSING] official checkpoint: {missing_path.resolve()} (discovery: {source_note})")
        all_ok = False
    else:
        size = file_size_bytes(checkpoint)
        print(
            f"[OK] official checkpoint: {checkpoint.resolve()}, "
            f"size={format_size(size)}, discovery={source_note}"
        )

    if all_ok:
        print("[OK] stage1 path/artifact audit passed")
        return 0

    print("[FAIL] stage1 path/artifact audit failed")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
