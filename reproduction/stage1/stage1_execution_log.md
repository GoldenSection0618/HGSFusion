# HGSFusion Stage 1 Execution Log

This file is an append-only command/result log for Stage 1.

Stage 1 scope:
- checkpoint/config/model-build validation
- official checkpoint audit
- single-batch forward dry run
- optional 1-2 batch eval dry run

Out of scope:
- full training
- full benchmark evaluation
- paper metric reproduction
- modifying root README.md
- modifying README_UPSTREAM.md
- modifying reproduction/stage0/
- committing data artifacts, checkpoints, raw datasets, or data symlinks

## Execution Log

### 2026-05-13T20:38:53+08:00
- current branch: `hgsfusion-stage1-model-runtime-dryrun`
- working directory: `/home/user/HGSFusion_research/HGSFusion`
- command block executed:
  ```bash
  mkdir -p reproduction/stage1/scripts
  cat > reproduction/stage1/stage1_execution_log.md <<'EOF'
  ... Stage 1 execution log header ...
  EOF
  cat > reproduction/stage1/stage1_reproduction_notes.md <<'EOF'
  ... Stage 1 reproduction notes initial content ...
  EOF
  ```
- exit status: `0`
- important output excerpt:
  - Stage 1 directory created: `reproduction/stage1/`
  - Stage 1 scripts directory created: `reproduction/stage1/scripts/`
  - Stage 1 docs initialized:
    - `reproduction/stage1/stage1_execution_log.md`
    - `reproduction/stage1/stage1_reproduction_notes.md`
- files changed:
  - `reproduction/stage1/stage1_execution_log.md`
  - `reproduction/stage1/stage1_reproduction_notes.md`
- reason: initialize Stage 1 directory structure and baseline docs before runtime checks.
- next action or blocker: run baseline environment and git-state check, then append the results.

### 2026-05-13T20:41:10+08:00
- current branch: `hgsfusion-stage1-model-runtime-dryrun`
- working directory: `/home/user/HGSFusion_research/HGSFusion`
- command block executed:
  ```bash
  cd /home/user/HGSFusion_research/HGSFusion
  pwd
  git branch --show-current
  git status --short
  git log --oneline -5

  source /home/user/miniforge3/etc/profile.d/conda.sh
  conda activate hgsfusion_a17

  export HGSFUSION_WORKDIR=/home/user/HGSFusion_research
  export HGSFUSION_REPO=/home/user/HGSFusion_research/HGSFusion
  export HGSFUSION_DATA_ROOT=/home/user/HGSFusion_research/HGSFusion/data
  export CUDA_HOME=/usr/local/cuda-11.7
  export PATH=/usr/local/cuda-11.7/bin:$PATH
  export LD_LIBRARY_PATH=$CONDA_PREFIX/lib:$CONDA_PREFIX/lib/python3.9/site-packages/torch/lib:/usr/local/cuda-11.7/lib64:${LD_LIBRARY_PATH:-}
  hash -r

  which python
  python --version
  python - <<'PY'
  import torch
  import mmcv
  import mmengine
  import mmdet
  print('torch:', torch.__version__)
  print('torch.version.cuda:', torch.version.cuda)
  print('torch.cuda.is_available:', torch.cuda.is_available())
  print('mmcv:', mmcv.__version__)
  print('mmengine:', mmengine.__version__)
  print('mmdet:', mmdet.__version__)
  PY

  echo "CUDA_HOME=${CUDA_HOME:-}"
  which nvcc
  nvcc --version
  ```
- exit status: `0`
- important output excerpt:
  - branch: `hgsfusion-stage1-model-runtime-dryrun`
  - working tree: clean (`git status --short` no output)
  - python: `/home/user/miniforge3/envs/hgsfusion_a17/bin/python`
  - python version: `3.9.23`
  - torch: `1.13.1+cu117`, `torch.version.cuda=11.7`, `torch.cuda.is_available=True`
  - mmcv: `2.1.0`, mmengine: `0.10.7`, mmdet: `3.3.0`
  - `CUDA_HOME=/usr/local/cuda-11.7`
  - `nvcc=/usr/local/cuda-11.7/bin/nvcc`, release `11.7`
- files changed:
  - `reproduction/stage1/stage1_execution_log.md`
- reason: baseline environment and git state verification before model-runtime checks.
- next action or blocker: re-run Stage 0 smoke check as Stage 1 baseline probe.

### 2026-05-13T20:42:03+08:00
- current branch: `hgsfusion-stage1-model-runtime-dryrun`
- working directory: `/home/user/HGSFusion_research/HGSFusion`
- command block executed:
  ```bash
  cd /home/user/HGSFusion_research/HGSFusion
  source /home/user/miniforge3/etc/profile.d/conda.sh
  conda activate hgsfusion_a17

  export HGSFUSION_WORKDIR=/home/user/HGSFusion_research
  export HGSFUSION_REPO=/home/user/HGSFusion_research/HGSFusion
  export HGSFUSION_DATA_ROOT=/home/user/HGSFusion_research/HGSFusion/data
  export CUDA_HOME=/usr/local/cuda-11.7
  export PATH=/usr/local/cuda-11.7/bin:$PATH
  export LD_LIBRARY_PATH=$CONDA_PREFIX/lib:$CONDA_PREFIX/lib/python3.9/site-packages/torch/lib:/usr/local/cuda-11.7/lib64:${LD_LIBRARY_PATH:-}
  hash -r

  python reproduction/stage0/scripts/hgsfusion_smoke_check.py
  ```
- exit status: `0`
- important output excerpt:
  - smoke script result: `SMOKE CHECK PASSED`
  - environment checks passed (`torch 1.13.1+cu117`, `torch.cuda.is_available=True`, `nvcc 11.7`)
  - import checks passed (`pcdet`, dataset modules, CUDA ops, `pillar_cuda`)
  - config load checks passed (`hgsfusion_vod.yaml`, `hgsfusion_tj4d.yaml`)
  - data interface checks passed for VoD/TJ4D `kitti_infos_{train,val}.pkl` and official hybrid point directories
  - noted warnings: `NumbaDeprecationWarning` from legacy jit decorators (non-blocking)
- files changed:
  - `reproduction/stage1/stage1_execution_log.md`
- reason: re-run Stage 0 smoke as Stage 1 baseline probe.
- next action or blocker: start Stage 1A (VoD) path/artifact audit.

### 2026-05-13T20:44:56+08:00
- current branch: `hgsfusion-stage1-model-runtime-dryrun`
- working directory: `/home/user/HGSFusion_research/HGSFusion`
- command block executed:
  ```bash
  # create Stage 1 path/artifact audit script
  cat > reproduction/stage1/scripts/stage1_path_artifact_audit.py <<'EOF_SCRIPT'
  ... stage1_path_artifact_audit.py ...
  EOF_SCRIPT
  chmod +x reproduction/stage1/scripts/stage1_path_artifact_audit.py

  source /home/user/miniforge3/etc/profile.d/conda.sh
  conda activate hgsfusion_a17
  export HGSFUSION_REPO=/home/user/HGSFusion_research/HGSFusion
  python reproduction/stage1/scripts/stage1_path_artifact_audit.py --dataset vod
  ```
- exit status: `0`
- important output excerpt:
  - `[OK]` config paths:
    - `tools/cfgs/hgsfusion/hgsfusion_vod.yaml`
    - `tools/cfgs/dataset_configs/vod_fusion.yaml`
  - `[OK]` data paths:
    - `data/vod_radar_5frames`
    - `data/vod_radar_5frames/kitti_infos_val.pkl`
    - `data/vod_radar_5frames/training/mask_maskformer_with_label_k_1_gauss_k_4_uniform`
  - `[OK]` DeepLabV3 pretrained:
    - `/home/user/HGSFusion_research/checkpoints/deeplabv3_resnet101_coco-586e9e4e.pth`
    - size `233.22MB`
  - `[OK]` official VoD checkpoint:
    - link path: `/home/user/HGSFusion_research/checkpoints/hgsfusion_vod.pth`
    - resolved target: `/mnt/e/HGSFusion_datasets/raw/hgsfusion_official_assets/hgsfusion_vod.pth`
    - size `274.93MB`
- files changed:
  - `reproduction/stage1/scripts/stage1_path_artifact_audit.py`
  - `reproduction/stage1/stage1_execution_log.md`
- reason: Stage 1A.10.1 VoD path and artifact audit.
- next action or blocker: implement and run VoD batch contract check (`batch_size=1`, `workers=0`, `training=False`).

### 2026-05-13T20:45:22+08:00
- current branch: `hgsfusion-stage1-model-runtime-dryrun`
- working directory: `/home/user/HGSFusion_research/HGSFusion`
- command block executed:
  ```bash
  cat > reproduction/stage1/scripts/stage1_batch_contract_check.py <<'EOF_SCRIPT'
  ... stage1_batch_contract_check.py ...
  EOF_SCRIPT
  chmod +x reproduction/stage1/scripts/stage1_batch_contract_check.py

  source /home/user/miniforge3/etc/profile.d/conda.sh
  conda activate hgsfusion_a17
  export HGSFUSION_REPO=/home/user/HGSFusion_research/HGSFusion
  python reproduction/stage1/scripts/stage1_batch_contract_check.py --dataset vod --batch-size 1 --workers 0
  ```
- exit status: `0`
- important output excerpt:
  - dataloader built with `batch_size=1`, `workers=0`, `training=False`, dataset_len=`1296`
  - batch keys:
    - `batch_size`, `calib`, `frame_id`, `gt_boxes`, `gt_boxes2d`, `image_shape`, `images`, `lidar_aug_matrix`, `points`, `trans_cam_to_img`, `trans_lidar_to_cam`, `use_lead_xyz`
  - required runtime keys for CaDDN/FusionVFE/ImageVFE present:
    - `points`, `images`, `image_shape`, `trans_lidar_to_cam`, `trans_cam_to_img`, `lidar_aug_matrix`, `frame_id`, `batch_size`
  - key-shape examples:
    - `points`: `(2591, 18)` `float64`
    - `images`: `(1, 1216, 1936, 3)` `float32`
    - `gt_boxes`: `(1, 7, 8)` `float32`
    - `gt_boxes2d`: `(1, 7, 4)` `float32`
  - compatibility notes:
    - `calib_matricies` not a direct batch key in this fork; model path uses `trans_lidar_to_cam` + `trans_cam_to_img`
    - `metadata` missing in current eval batch; `calib` + `frame_id` are present
  - `kornia` import check: passed
- files changed:
  - `reproduction/stage1/scripts/stage1_batch_contract_check.py`
  - `reproduction/stage1/stage1_execution_log.md`
- reason: Stage 1A.10.2 VoD batch contract check.
- next action or blocker: Stage 1A.10.3 VoD model build-only check.
