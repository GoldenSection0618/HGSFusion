#!/usr/bin/env python3
import os
import platform
import subprocess
import sys
from pathlib import Path


def run_cmd(cmd):
    try:
        out = subprocess.check_output(cmd, stderr=subprocess.STDOUT, text=True).strip()
        return True, out
    except Exception as e:
        return False, repr(e)


def resolve_repo_root():
    env_repo = os.environ.get("HGSFUSION_REPO")
    if env_repo:
        p = Path(env_repo).expanduser().resolve()
        if p.exists():
            return p

    script_dir = Path(__file__).resolve().parent
    git_ok, git_root = run_cmd(["git", "-C", str(script_dir), "rev-parse", "--show-toplevel"])
    if git_ok:
        return Path(git_root)

    for parent in script_dir.parents:
        if (parent / "pcdet").exists() and (parent / "tools/cfgs/hgsfusion").exists():
            return parent

    return Path.cwd()


def check_path(path: Path, required=True):
    ok = path.exists()
    status = "OK" if ok else ("MISSING" if required else "OPTIONAL-MISSING")
    print(f"[{status}] {path}")
    return ok or (not required)


def check_import(name, required=True):
    try:
        __import__(name)
        print(f"[OK] import {name}")
        return True
    except Exception as e:
        status = "FAIL" if required else "WARN"
        print(f"[{status}] import {name}: {e!r}")
        return not required


def check_config(config_path):
    try:
        from pcdet.config import cfg, cfg_from_yaml_file

        cfg_from_yaml_file(str(config_path), cfg)
        print(f"[OK] config load {config_path}")
        return True
    except Exception as e:
        print(f"[FAIL] config load {config_path}: {e!r}")
        return False


def main():
    repo_root = resolve_repo_root()
    shared_data_root = Path("/home/user/HGSFusion_research/data")
    local_data_link = repo_root / "data"
    ok = True
    original_cwd = Path.cwd()
    if original_cwd != repo_root:
        os.chdir(repo_root)

    print("== Python/CUDA Environment ==")
    print(f"python: {sys.version.split()[0]} ({sys.executable})")
    print(f"platform: {platform.platform()}")

    try:
        import torch
        from torch.utils.cpp_extension import CUDA_HOME as TORCH_CUDA_HOME

        print(f"torch: {torch.__version__}")
        print(f"torch.version.cuda: {torch.version.cuda}")
        print(f"torch.cuda.is_available: {torch.cuda.is_available()}")
        print(f"torch CUDA_HOME: {TORCH_CUDA_HOME}")
    except Exception as e:
        print(f"[FAIL] torch diagnostics: {e!r}")
        return 1

    print(f"shell CUDA_HOME: {os.environ.get('CUDA_HOME', '')}")
    which_ok, which_nvcc = run_cmd(["bash", "-lc", "which nvcc"])
    print(f"which nvcc: {which_nvcc if which_ok else 'not found'}")
    nvcc_ok, nvcc_ver = run_cmd(["bash", "-lc", "nvcc --version"])
    print("nvcc --version:")
    print(nvcc_ver)
    if not which_ok or "cuda-11.7" not in which_nvcc:
        print("[WARN] nvcc path is not explicitly from /usr/local/cuda-11.7")

    print("\n== Imports ==")
    ok &= check_import("pcdet")
    ok &= check_import("pcdet.datasets")
    ok &= check_import("pcdet.datasets.kitti.vod_dataset")
    ok &= check_import("pcdet.datasets.kitti.tj4d_dataset")
    ok &= check_import("pcdet.ops.iou3d_nms.iou3d_nms_cuda")
    ok &= check_import("pcdet.ops.roiaware_pool3d.roiaware_pool3d_cuda")
    ok &= check_import("pcdet.ops.pointnet2.pointnet2_stack.pointnet2_stack_cuda")
    ok &= check_import("pillar_cuda", required=False)

    print("\n== Config Load ==")
    ok &= check_config(repo_root / "tools/cfgs/hgsfusion/hgsfusion_vod.yaml")
    ok &= check_config(repo_root / "tools/cfgs/hgsfusion/hgsfusion_tj4d.yaml")

    print("\n== Data Interface ==")
    ok &= check_path(shared_data_root)
    if local_data_link.is_symlink():
        print(f"[OK] symlink {local_data_link} -> {os.readlink(local_data_link)}")
    else:
        print(f"[WARN] {local_data_link} is not a symlink")

    ok &= check_path(local_data_link / "vod_radar_5frames")
    ok &= check_path(local_data_link / "tj4d")

    vod_info_train = local_data_link / "vod_radar_5frames/kitti_infos_train.pkl"
    vod_info_val = local_data_link / "vod_radar_5frames/kitti_infos_val.pkl"
    tj4d_info_train = local_data_link / "tj4d/kitti_infos_train.pkl"
    tj4d_info_val = local_data_link / "tj4d/kitti_infos_val.pkl"
    ok &= check_path(vod_info_train)
    ok &= check_path(vod_info_val)
    ok &= check_path(tj4d_info_train)
    ok &= check_path(tj4d_info_val)

    ok &= check_path(local_data_link / "vod_radar_5frames/training/mask_maskformer_with_label_k_1_gauss_k_4_uniform")
    ok &= check_path(local_data_link / "tj4d/training/mask_maskformer_with_label_k_1_gauss_k_4_uniform")

    print("\n== Result ==")
    if ok:
        print("SMOKE CHECK PASSED")
        if Path.cwd() != original_cwd:
            os.chdir(original_cwd)
        return 0
    print("SMOKE CHECK FAILED")
    if Path.cwd() != original_cwd:
        os.chdir(original_cwd)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
