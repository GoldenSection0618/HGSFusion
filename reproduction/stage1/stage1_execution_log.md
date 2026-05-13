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
