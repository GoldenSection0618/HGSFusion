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

### 2026-05-13T20:52:40+08:00
- current branch: `hgsfusion-stage1-model-runtime-dryrun`
- working directory: `/home/user/HGSFusion_research/HGSFusion`
- command block executed:
  ```bash
  cat > reproduction/stage1/scripts/stage1_checkpoint_audit.py <<'EOF_SCRIPT'
  ... stage1_checkpoint_audit.py ...
  EOF_SCRIPT
  chmod +x reproduction/stage1/scripts/stage1_checkpoint_audit.py

  # first build-only attempt
  python reproduction/stage1/scripts/stage1_checkpoint_audit.py --dataset vod --mode build-only
  ```
- exit status: `1`
- important output excerpt:
  - failure traceback:
    - `ModuleNotFoundError: No module named 'spconv'`
  - failure stage: `from pcdet.models import build_network` during model import chain.
- files changed:
  - `reproduction/stage1/scripts/stage1_checkpoint_audit.py`
  - `reproduction/stage1/stage1_execution_log.md`
- reason: Stage 1A.10.3 VoD model build-only check initialization and first blocker capture.
- next action or blocker: install missing runtime dependency `spconv` compatible with torch1.13/cu117, then retry.

### 2026-05-13T20:53:16+08:00
- current branch: `hgsfusion-stage1-model-runtime-dryrun`
- working directory: `/home/user/HGSFusion_research/HGSFusion`
- command block executed:
  ```bash
  source /home/user/miniforge3/etc/profile.d/conda.sh
  conda activate hgsfusion_a17
  python -m pip install spconv-cu117

  python reproduction/stage1/scripts/stage1_checkpoint_audit.py --dataset vod --mode build-only
  ```
- exit status: `1`
- important output excerpt:
  - dependency install success:
    - `spconv-cu117-2.3.6`
    - `cumm-cu117-0.4.11`
  - second build-only attempt failed with import traceback:
    - `ModuleNotFoundError: No module named 'pcdet.models.backbones_3d.vfe.feature_sampler'`
- files changed:
  - `reproduction/stage1/stage1_execution_log.md`
- reason: resolve first runtime dependency blocker and re-run build-only check.
- next action or blocker: apply minimal compatibility import fix in `pcdet/models/backbones_3d/vfe/fusion_vfe.py`.

### 2026-05-13T20:54:06+08:00
- current branch: `hgsfusion-stage1-model-runtime-dryrun`
- working directory: `/home/user/HGSFusion_research/HGSFusion`
- command block executed:
  ```bash
  # minimal fix 1
  # remove nonexistent feature_sampler import, keep backward-compatible alias
  # 'GaussianSampler' -> SimpleSampler in feature_sampler map

  python reproduction/stage1/scripts/stage1_checkpoint_audit.py --dataset vod --mode build-only
  ```
- exit status: `1`
- important output excerpt:
  - previous `feature_sampler` import issue resolved.
  - new import traceback:
    - `ModuleNotFoundError: No module named 'pcdet.models.backbones_3d.vfe.radar_occupancy_2d'`
- files changed:
  - `pcdet/models/backbones_3d/vfe/fusion_vfe.py`
  - `reproduction/stage1/stage1_execution_log.md`
- reason: minimal import compatibility fix required by Stage 1 model build.
- next action or blocker: make `RadarOccupancy2D` optional import in `fusion_vfe.py` while preserving existing `RadarOccupancy2DV2` path.

### 2026-05-13T20:54:56+08:00
- current branch: `hgsfusion-stage1-model-runtime-dryrun`
- working directory: `/home/user/HGSFusion_research/HGSFusion`
- command block executed:
  ```bash
  # minimal fix 2
  # make RadarOccupancy2D optional import; keep map for available classes

  python reproduction/stage1/scripts/stage1_checkpoint_audit.py --dataset vod --mode build-only
  ```
- exit status: `1`
- important output excerpt:
  - `RadarOccupancy2D` import blocker resolved.
  - new import traceback:
    - `ModuleNotFoundError: No module named 'pcdet.models.backbones_3d.vfe.foreground_sampler'`
- files changed:
  - `pcdet/models/backbones_3d/vfe/fusion_vfe.py`
  - `reproduction/stage1/stage1_execution_log.md`
- reason: continue minimal compatibility repair chain discovered during model import.
- next action or blocker: make `ForegroundSampler` optional import and only hard-fail if config explicitly enables it.

### 2026-05-13T20:55:43+08:00
- current branch: `hgsfusion-stage1-model-runtime-dryrun`
- working directory: `/home/user/HGSFusion_research/HGSFusion`
- command block executed:
  ```bash
  # minimal fix 3
  # make ForegroundSampler optional import; guard only when config requests it

  python reproduction/stage1/scripts/stage1_checkpoint_audit.py --dataset vod --mode build-only
  python reproduction/stage1/scripts/stage1_checkpoint_audit.py --dataset vod --mode audit --ckpt /home/user/HGSFusion_research/checkpoints/hgsfusion_vod.pth
  ```
- exit status: `0`
- important output excerpt:
  - build-only result:
    - model class: `CaDDN`
    - module_list classes: `FusionVFE`, `FusionAfterBEVSEDirect`, `AnchorHeadSingle`
    - `len(model.state_dict()) = 936`
    - deeplab cfg path resolved to `/home/user/HGSFusion_research/checkpoints/deeplabv3_resnet101_coco-586e9e4e.pth`, exists.
  - checkpoint audit result:
    - checkpoint keys: `['epoch', 'it', 'model_state', 'optimizer_state', 'version']`
    - `len(checkpoint['model_state']) = 936`
    - matched: `936`
    - missing: `0`
    - unexpected: `0`
    - shape mismatch: `0`
    - matched ratio: `1.000000`
- files changed:
  - `pcdet/models/backbones_3d/vfe/fusion_vfe.py`
  - `reproduction/stage1/stage1_execution_log.md`
- reason: complete Stage 1A.10.3 model build and Stage 1A.10.4 checkpoint structural audit for VoD.
- next action or blocker: run Stage 1A.10.5 official checkpoint load via repository loading path.

### 2026-05-13T20:56:29+08:00
- current branch: `hgsfusion-stage1-model-runtime-dryrun`
- working directory: `/home/user/HGSFusion_research/HGSFusion`
- command block executed:
  ```bash
  python - <<'PY'
  from pcdet.config import cfg, cfg_from_yaml_file
  from pcdet.datasets import build_dataloader
  from pcdet.models import build_network
  from pcdet.utils import common_utils

  cfg_from_yaml_file('tools/cfgs/hgsfusion/hgsfusion_vod.yaml', cfg)
  logger = common_utils.create_logger()
  dataset, loader, _ = build_dataloader(..., batch_size=1, workers=0, training=False)
  model = build_network(model_cfg=cfg.MODEL, num_class=len(cfg.CLASS_NAMES), dataset=dataset)
  model.load_params_from_file(filename='/home/user/HGSFusion_research/checkpoints/hgsfusion_vod.pth', logger=logger, to_cpu=True)
  print('CHECKPOINT_LOAD_DONE')
  PY
  ```
- exit status: `0`
- important output excerpt:
  - loader output:
    - `==> Loading parameters from checkpoint ... to CPU`
    - `==> Checkpoint trained from version: pcdet+0.6.0+988049d+py6e93e5a`
    - `==> Done (loaded 936/936)`
  - no missing/unexpected update warning emitted by loader.
- files changed:
  - `reproduction/stage1/stage1_execution_log.md`
- reason: Stage 1A.10.5 VoD checkpoint load verification using repository-standard load path.
- next action or blocker: run Stage 1A.10.6 single-batch forward script.

### 2026-05-13T20:57:33+08:00
- current branch: `hgsfusion-stage1-model-runtime-dryrun`
- working directory: `/home/user/HGSFusion_research/HGSFusion`
- command block executed:
  ```bash
  cat > reproduction/stage1/scripts/stage1_single_batch_forward.py <<'EOF_SCRIPT'
  ... stage1_single_batch_forward.py ...
  EOF_SCRIPT
  chmod +x reproduction/stage1/scripts/stage1_single_batch_forward.py

  # first run
  python reproduction/stage1/scripts/stage1_single_batch_forward.py --dataset vod --batch-size 1 --workers 0
  ```
- exit status: `-1`
- important output excerpt:
  - checkpoint loading on GPU succeeded (`loaded 936/936`).
  - forward failed at runtime library stage:
    - `Could not load library libcudnn_cnn_infer.so.8. Error: libcuda.so: cannot open shared object file: No such file or directory`
- files changed:
  - `reproduction/stage1/scripts/stage1_single_batch_forward.py`
  - `reproduction/stage1/stage1_execution_log.md`
- reason: Stage 1A.10.6 initial single-batch forward attempt.
- next action or blocker: fix runtime library path by adding `/usr/lib/wsl/lib` to `LD_LIBRARY_PATH` and rerun.

### 2026-05-13T20:58:34+08:00
- current branch: `hgsfusion-stage1-model-runtime-dryrun`
- working directory: `/home/user/HGSFusion_research/HGSFusion`
- command block executed:
  ```bash
  export CUDA_HOME=/usr/local/cuda-11.7
  export PATH=/usr/local/cuda-11.7/bin:$PATH
  export LD_LIBRARY_PATH=$CONDA_PREFIX/lib:$CONDA_PREFIX/lib/python3.9/site-packages/torch/lib:/usr/local/cuda-11.7/lib64:/usr/lib/wsl/lib:${LD_LIBRARY_PATH:-}
  python reproduction/stage1/scripts/stage1_single_batch_forward.py --dataset vod --batch-size 1 --workers 0
  ```
- exit status: `0`
- important output excerpt:
  - checkpoint load: `==> Done (loaded 936/936)`
  - forward output schema:
    - `pred_dicts` type: `list`
    - `len(pred_dicts) = 1`
    - pred keys: `pred_boxes`, `pred_scores`, `pred_labels`
    - `pred_boxes`: `(3, 7)`
    - `pred_scores`: `(3,)`
    - `pred_labels`: `(3,)`
    - `recall_dict` keys: `gt`, `roi_0.3`, `rcnn_0.3`, `roi_0.5`, `rcnn_0.5`, `roi_0.7`, `rcnn_0.7`
- files changed:
  - `reproduction/stage1/stage1_execution_log.md`
- reason: Stage 1A.10.6 VoD single-batch forward pass verification.
- next action or blocker: Stage 1A.10.7 optional 1-2 batch eval dry run.

### 2026-05-13T20:59:30+08:00
- current branch: `hgsfusion-stage1-model-runtime-dryrun`
- working directory: `/home/user/HGSFusion_research/HGSFusion`
- command block executed:
  ```bash
  # optional VoD 2-batch eval dry run (no eval_one_epoch, no output files)
  python - <<'PY'
  ... limited loop over max_batches=2 with load_data_to_gpu + model(batch) ...
  PY
  ```
- exit status: `0`
- important output excerpt:
  - `BATCH_0_OK pred_boxes=3`
  - `BATCH_1_OK pred_boxes=12`
  - `EVAL_DRYRUN_OK [3, 12]`
  - no evaluation artifacts or result files were written by this limited loop.
- files changed:
  - `reproduction/stage1/stage1_execution_log.md`
- reason: Stage 1A.10.7 optional limited eval dry run after single-batch forward success.
- next action or blocker: start Stage 1B (TJ4D) checks in the same sequence.

### 2026-05-13T21:00:28+08:00
- current branch: `hgsfusion-stage1-model-runtime-dryrun`
- working directory: `/home/user/HGSFusion_research/HGSFusion`
- command block executed:
  ```bash
  python reproduction/stage1/scripts/stage1_path_artifact_audit.py --dataset tj4d
  python reproduction/stage1/scripts/stage1_batch_contract_check.py --dataset tj4d --batch-size 1 --workers 0
  ```
- exit status: `0`
- important output excerpt:
  - TJ4D path/artifact audit passed:
    - `tools/cfgs/hgsfusion/hgsfusion_tj4d.yaml`
    - `tools/cfgs/dataset_configs/tj4d_fusion.yaml`
    - `data/tj4d/kitti_infos_val.pkl`
    - official hybrid points dir
    - deeplab checkpoint
    - official TJ4D checkpoint (`/mnt/e/.../hgsfusion_tj4d.pth`)
  - TJ4D batch contract passed:
    - batch keys include `points/images/gt_boxes/gt_boxes2d/trans_lidar_to_cam/trans_cam_to_img/lidar_aug_matrix`
    - `calib_matricies` absent but compatibility mapping to trans matrices confirmed
    - `metadata` absent in eval batch; `calib` + `frame_id` present
- files changed:
  - `reproduction/stage1/stage1_execution_log.md`
- reason: Stage 1B path/artifact and batch contract checks for TJ4D.
- next action or blocker: run TJ4D model build-only and checkpoint audit.

### 2026-05-13T21:01:24+08:00
- current branch: `hgsfusion-stage1-model-runtime-dryrun`
- working directory: `/home/user/HGSFusion_research/HGSFusion`
- command block executed:
  ```bash
  python reproduction/stage1/scripts/stage1_checkpoint_audit.py --dataset tj4d --mode build-only
  python reproduction/stage1/scripts/stage1_checkpoint_audit.py --dataset tj4d --mode audit --ckpt /home/user/HGSFusion_research/checkpoints/hgsfusion_tj4d.pth
  ```
- exit status: `0`
- important output excerpt:
  - build-only:
    - model class: `CaDDN`
    - module_list classes: `FusionVFE`, `FusionAfterBEVSEDirect`, `AnchorHeadSingle`
    - `len(model.state_dict()) = 936`
    - deeplab resolved path exists
  - checkpoint audit:
    - checkpoint keys: `['epoch', 'it', 'model_state', 'optimizer_state', 'version']`
    - `len(checkpoint['model_state']) = 936`
    - matched: `936`
    - missing/unexpected/shape-mismatch: `0/0/0`
    - matched ratio: `1.000000`
- files changed:
  - `reproduction/stage1/stage1_execution_log.md`
- reason: complete Stage 1B model build and checkpoint structural audit.
- next action or blocker: run repository-path checkpoint load and single-batch forward for TJ4D.

### 2026-05-13T21:02:22+08:00
- current branch: `hgsfusion-stage1-model-runtime-dryrun`
- working directory: `/home/user/HGSFusion_research/HGSFusion`
- command block executed:
  ```bash
  # checkpoint load (repository path)
  python - <<'PY'
  ... build model from hgsfusion_tj4d.yaml ...
  model.load_params_from_file('/home/user/HGSFusion_research/checkpoints/hgsfusion_tj4d.pth', to_cpu=True)
  print('CHECKPOINT_LOAD_DONE')
  PY

  # single-batch forward
  export LD_LIBRARY_PATH=...:/usr/lib/wsl/lib:...
  python reproduction/stage1/scripts/stage1_single_batch_forward.py --dataset tj4d --batch-size 1 --workers 0
  ```
- exit status: `0`
- important output excerpt:
  - checkpoint loader summary:
    - `==> Done (loaded 936/936)`
  - single-batch forward output schema:
    - `pred_dicts` list with len `1`
    - `pred_boxes` `(3, 7)`
    - `pred_scores` `(3,)`
    - `pred_labels` `(3,)`
    - recall keys include `gt/roi_*/rcnn_*`
- files changed:
  - `reproduction/stage1/stage1_execution_log.md`
- reason: complete Stage 1B checkpoint load and single-batch forward validation.
- next action or blocker: run optional TJ4D 1-2 batch eval dry run.

### 2026-05-13T21:03:17+08:00
- current branch: `hgsfusion-stage1-model-runtime-dryrun`
- working directory: `/home/user/HGSFusion_research/HGSFusion`
- command block executed:
  ```bash
  # optional TJ4D 2-batch eval dry run (no eval_one_epoch, no output files)
  python - <<'PY'
  ... limited loop over max_batches=2 with load_data_to_gpu + model(batch) ...
  PY
  ```
- exit status: `0`
- important output excerpt:
  - `BATCH_0_OK pred_boxes=3`
  - `BATCH_1_OK pred_boxes=6`
  - `EVAL_DRYRUN_OK [3, 6]`
  - no evaluation artifacts or result files were written by this limited loop.
- files changed:
  - `reproduction/stage1/stage1_execution_log.md`
- reason: Stage 1B optional limited eval dry run.
- next action or blocker: consolidate Stage 1 notes/scripts status and finalize Stage 1 deliverables.
