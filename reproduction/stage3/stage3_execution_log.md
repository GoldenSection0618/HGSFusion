# HGSFusion Stage 3 Execution Log

This file is an append-only command/result log for Stage 3.

Stage 3 scope:
- full VoD official-checkpoint evaluation through `tools/test.py`
- full TJ4D official-checkpoint evaluation through `tools/test.py`
- full artifact contract validation
- metric parsing and structured summary generation

Out of scope:
- full training
- paper-level metric reproduction claim
- distributed evaluation
- TTA evaluation
- modifying `README.md`
- modifying `README_UPSTREAM.md`
- modifying `reproduction/stage0/`
- modifying `reproduction/stage1/`
- modifying `reproduction/stage2/`

## Execution Log

### 2026-05-14T08:43:47+08:00
- current branch: `hgsfusion-stage3-full-official-eval`
- working directory: `/home/user/HGSFusion_research/HGSFusion`
- command block executed:
  ```bash
  sed -n '1,220p' HGSFusion/AGENT.md
  sed -n '221,520p' HGSFusion/AGENT.md
  sed -n '521,920p' HGSFusion/AGENT.md
  sed -n '921,1320p' HGSFusion/AGENT.md
  ```
- exit status: `0`
- important output excerpt:
  - Loaded full Stage 3 instruction contract from `HGSFusion/AGENT.md`
  - Confirmed strict README/stage0-2 immutability and Stage 3 incremental commit requirements
  - Confirmed required Stage 3 scripts/configs/log/note structure and evaluation pass criteria
- files changed:
  - none (read-only)
- reason: read authoritative Stage 3 execution instructions before any Stage 3 write operation
- next action or blocker: run branch/state checks and ensure write operations are only on Stage 3 branch

### 2026-05-14T08:43:47+08:00
- current branch: `hgsfusion-stage3-full-official-eval`
- working directory: `/home/user/HGSFusion_research/HGSFusion`
- command block executed:
  ```bash
  cd /home/user/HGSFusion_research
  pwd
  ls -la
  cd /home/user/HGSFusion_research/HGSFusion
  pwd
  git branch --show-current
  git status --short
  git log --oneline --decorate -10

  git switch main
  git pull --ff-only
  git status --short
  git switch hgsfusion-stage3-full-official-eval
  git branch --show-current
  git status --short
  git log --oneline --decorate -10
  git diff -- README.md README_UPSTREAM.md reproduction/stage0 reproduction/stage1 reproduction/stage2 || true
  ```
- exit status: `0`
- important output excerpt:
  - `main` updated successfully (`Already up to date`)
  - switched back to `hgsfusion-stage3-full-official-eval`
  - working tree clean before Stage 3 initialization
  - no diffs in `README.md`, `README_UPSTREAM.md`, `reproduction/stage0`, `reproduction/stage1`, `reproduction/stage2`
- files changed:
  - none (read-only)
- reason: satisfy Stage 3 branch discipline and baseline immutability precondition before any writes
- next action or blocker: complete required Stage 0/1/2 baseline pre-reading

### 2026-05-14T08:43:47+08:00
- current branch: `hgsfusion-stage3-full-official-eval`
- working directory: `/home/user/HGSFusion_research/HGSFusion`
- command block executed:
  ```bash
  sed -n '1,260p' reproduction/stage0/stage0_reproduction_notes.md
  sed -n '1,320p' reproduction/stage1/stage1_reproduction_notes.md
  sed -n '1,360p' reproduction/stage2/stage2_reproduction_notes.md
  sed -n '1,260p' reproduction/stage2/stage2_execution_log.md
  ```
- exit status: `0`
- important output excerpt:
  - Confirmed environment convention (`conda activate hgsfusion_a17`, CUDA 11.7, `LD_LIBRARY_PATH` includes WSL CUDA path)
  - Confirmed Stage 2 fix boundary is evaluation-finalization path, not model topology/hyperparameters
  - Confirmed TJ4D split interpretation must be `official eval split / test-val alias split`
  - Confirmed artifact policy and non-commit runtime outputs policy
- files changed:
  - none (read-only)
- reason: establish Stage 3 dependency baseline per required pre-reading section
- next action or blocker: initialize `reproduction/stage3` structure and template docs

### 2026-05-14T08:43:47+08:00
- current branch: `hgsfusion-stage3-full-official-eval`
- working directory: `/home/user/HGSFusion_research/HGSFusion`
- command block executed:
  ```bash
  mkdir -p reproduction/stage3/scripts
  mkdir -p reproduction/stage3/local_cfgs
  create reproduction/stage3/stage3_execution_log.md
  create reproduction/stage3/stage3_reproduction_notes.md
  ```
- exit status: `0`
- important output excerpt:
  - Stage 3 directory skeleton created under `reproduction/stage3/`
  - initialized append-only log and Stage 3 notes template with required sections
- files changed:
  - `reproduction/stage3/stage3_execution_log.md`
  - `reproduction/stage3/stage3_reproduction_notes.md`
- reason: initialize mandatory Stage 3 record structure before evaluation tasks
- next action or blocker: commit initialization records, then run Stage 3 environment audit

### 2026-05-14T08:44:44+08:00
- current branch: `hgsfusion-stage3-full-official-eval`
- working directory: `/home/user/HGSFusion_research/HGSFusion`
- command block executed:
  ```bash
  cd /home/user/HGSFusion_research/HGSFusion
  source /home/user/miniforge3/etc/profile.d/conda.sh
  conda activate hgsfusion_a17

  export CUDA_VISIBLE_DEVICES=0
  export HGSFUSION_WORKDIR=/home/user/HGSFusion_research
  export HGSFUSION_REPO=/home/user/HGSFusion_research/HGSFusion
  export HGSFUSION_DATA_ROOT=/home/user/HGSFusion_research/HGSFusion/data
  export CUDA_HOME=/usr/local/cuda-11.7
  export PATH=/usr/local/cuda-11.7/bin:$PATH
  export LD_LIBRARY_PATH=$CONDA_PREFIX/lib:$CONDA_PREFIX/lib/python3.9/site-packages/torch/lib:/usr/local/cuda-11.7/lib64:/usr/lib/wsl/lib:${LD_LIBRARY_PATH:-}
  export PYTHONFAULTHANDLER=1
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
  - `python` = `/home/user/miniforge3/envs/hgsfusion_a17/bin/python`
  - `Python 3.9.23`
  - `torch 1.13.1+cu117`, `torch.version.cuda 11.7`, `torch.cuda.is_available True`
  - `mmcv 2.1.0`, `mmengine 0.10.7`, `mmdet 3.3.0`
  - `CUDA_HOME=/usr/local/cuda-11.7`
  - `nvcc release 11.7, V11.7.99`
- files changed:
  - `reproduction/stage3/stage3_execution_log.md`
- reason: verify Stage 3 runtime environment alignment before full evaluation
- next action or blocker: copy Stage 3 local full-eval configs and verify diffs

### 2026-05-14T08:45:06+08:00
- current branch: `hgsfusion-stage3-full-official-eval`
- working directory: `/home/user/HGSFusion_research/HGSFusion`
- command block executed:
  ```bash
  cp tools/cfgs/hgsfusion/hgsfusion_vod.yaml     reproduction/stage3/local_cfgs/hgsfusion_vod_stage3_full_eval.yaml

  cp tools/cfgs/hgsfusion/hgsfusion_tj4d.yaml     reproduction/stage3/local_cfgs/hgsfusion_tj4d_stage3_full_eval.yaml

  diff -u tools/cfgs/hgsfusion/hgsfusion_vod.yaml     reproduction/stage3/local_cfgs/hgsfusion_vod_stage3_full_eval.yaml || true

  diff -u tools/cfgs/hgsfusion/hgsfusion_tj4d.yaml     reproduction/stage3/local_cfgs/hgsfusion_tj4d_stage3_full_eval.yaml || true
  ```
- exit status: `0`
- important output excerpt:
  - both  commands produced no output
  - local Stage 3 cfg copies are functionally identical to official cfg files
- files changed:
  - 
  - 
  - 
- reason: create Stage 3 local cfg copies for full official-checkpoint evaluation without functional config drift
- next action or blocker: create Stage 3 evaluation contract checker script and run 

### 2026-05-14T08:45:29+08:00
- current branch: `hgsfusion-stage3-full-official-eval`
- working directory: `/home/user/HGSFusion_research/HGSFusion`
- command block executed:
  ```bash
  cat >> reproduction/stage3/stage3_execution_log.md <<EOF
  ... markdown with backticks ...
  EOF
  ```
- exit status: `0` (logical failure in content generation)
- important output excerpt:
  - shell attempted to execute text inside backticks due unquoted heredoc
  - stderr included `diff: missing operand after '-u'`, `Permission denied`, and `--help: command not found`
  - resulting appended entry at `2026-05-14T08:45:06+08:00` became partially malformed
- files changed:
  - `reproduction/stage3/stage3_execution_log.md` (malformed partial entry appended)
- reason: attempted to append config-step log entry using an unsafe heredoc quoting mode
- next action or blocker: append a corrected note with full config-step details using single-quoted heredoc; keep append-only history intact

### 2026-05-14T08:45:41+08:00
- current branch: `hgsfusion-stage3-full-official-eval`
- working directory: `/home/user/HGSFusion_research/HGSFusion`
- command block executed:
  ```bash
  cp tools/cfgs/hgsfusion/hgsfusion_vod.yaml     reproduction/stage3/local_cfgs/hgsfusion_vod_stage3_full_eval.yaml

  cp tools/cfgs/hgsfusion/hgsfusion_tj4d.yaml     reproduction/stage3/local_cfgs/hgsfusion_tj4d_stage3_full_eval.yaml

  diff -u tools/cfgs/hgsfusion/hgsfusion_vod.yaml     reproduction/stage3/local_cfgs/hgsfusion_vod_stage3_full_eval.yaml || true

  diff -u tools/cfgs/hgsfusion/hgsfusion_tj4d.yaml     reproduction/stage3/local_cfgs/hgsfusion_tj4d_stage3_full_eval.yaml || true
  ```
- exit status: `0`
- important output excerpt:
  - both diff checks returned no textual diff
  - Stage 3 local cfg copies are identical to source official cfgs
- files changed:
  - `reproduction/stage3/local_cfgs/hgsfusion_vod_stage3_full_eval.yaml`
  - `reproduction/stage3/local_cfgs/hgsfusion_tj4d_stage3_full_eval.yaml`
  - `reproduction/stage3/stage3_execution_log.md`
- reason: establish Stage 3 full-eval config copies while preserving official configuration behavior
- next action or blocker: implement Stage 3 contract checker script and validate CLI
