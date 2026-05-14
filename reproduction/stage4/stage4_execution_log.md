# HGSFusion Stage 4 Execution Log

This file is an append-only command/result log for Stage 4.

Stage 4 scope:
- bounded training-chain validation
- training=True dataloader validation
- training data contract validation
- controlled subset training smoke
- forward/backward/optimizer-step validation
- checkpoint save validation
- checkpoint resume validation
- train-after-eval artifact validation
- minimal DDP + SyncBN smoke if hardware allows

Out of scope:
- full VoD training reproduction
- full TJ4D training reproduction
- full benchmark reproduction
- paper metric reproduction
- TTA evaluation
- Mask2Former-based hybrid point generation
- modifying root README.md
- modifying README_UPSTREAM.md
- modifying reproduction/stage0/
- modifying reproduction/stage1/
- modifying reproduction/stage2/
- modifying reproduction/stage3/
- committing data artifacts, checkpoints, raw datasets, output artifacts, or data symlinks

## Execution Log

### 2026-05-14T16:14:06+08:00
- current branch: `hgsfusion-stage4-training-chain-validation`
- working directory: `/home/user/HGSFusion_research/HGSFusion`
- command block executed:
  ```bash
  cd /home/user/HGSFusion_research/HGSFusion
  git switch main
  git pull --ff-only
  git status --short
  git switch -c hgsfusion-stage4-training-chain-validation
  git branch --show-current
  pwd
  git branch --show-current
  git status --short
  git log --oneline -8
  find reproduction -maxdepth 2 -type f | sort
  git diff -- README.md README_UPSTREAM.md reproduction/stage0 reproduction/stage1 reproduction/stage2 reproduction/stage3
  mkdir -p reproduction/stage4/scripts reproduction/stage4/local_cfgs reproduction/stage4/outputs
  ```
- exit status: `0`
- important output excerpt:
  - branch switched from `main` to `hgsfusion-stage4-training-chain-validation`.
  - `git pull --ff-only` returned `Already up to date.`
  - `git status --short` was empty before Stage 4 initialization.
  - protected paths diff check returned empty output:
    - `README.md`
    - `README_UPSTREAM.md`
    - `reproduction/stage0/`
    - `reproduction/stage1/`
    - `reproduction/stage2/`
    - `reproduction/stage3/`
  - existing reproduction files include Stage 0/1/2/3 logs and Stage 3 metrics artifacts.
  - Stage 4 directories initialized:
    - `reproduction/stage4/scripts`
    - `reproduction/stage4/local_cfgs`
    - `reproduction/stage4/outputs`
- files changed:
  - `reproduction/stage4/stage4_execution_log.md`
  - `reproduction/stage4/stage4_reproduction_notes.md`
- reason: satisfy branch discipline and preflight immutability checks before any Stage 4 runtime commands.
- next action or blocker: initialize Stage 4 notes baseline content and commit Stage 4 doc initialization.

### 2026-05-14T16:15:20+08:00
- current branch: `hgsfusion-stage4-training-chain-validation`
- working directory: `/home/user/HGSFusion_research/HGSFusion`
- command block executed:
  ```bash
  git status --short
  git diff -- README.md
  git add reproduction/stage4/stage4_execution_log.md reproduction/stage4/stage4_reproduction_notes.md
  git commit -m "stage4: initialize training-chain validation docs"
  git rev-parse --short HEAD
  ```
- exit status: `0`
- important output excerpt:
  - `git status --short` showed only `?? reproduction/stage4/`.
  - `git diff -- README.md` returned empty output.
  - created commit: `7f2e0ef`.
  - commit message: `stage4: initialize training-chain validation docs`.
- files changed:
  - `reproduction/stage4/stage4_execution_log.md`
  - `reproduction/stage4/stage4_reproduction_notes.md`
- reason: commit Stage 4 docs immediately after initialization, as required.
- next action or blocker: run Stage 4 environment setup/verification and then implement Stage 4B scripts.

### 2026-05-14T17:01:21+08:00
- current branch: `hgsfusion-stage4-training-chain-validation`
- working directory: `/home/user/HGSFusion_research/HGSFusion`
- command block executed:
  ```bash
  source /home/user/miniforge3/etc/profile.d/conda.sh
  conda activate hgsfusion_a17
  export HGSFUSION_WORKDIR=/home/user/HGSFusion_research
  export HGSFUSION_REPO=/home/user/HGSFusion_research/HGSFusion
  export HGSFUSION_DATA_ROOT=/home/user/HGSFusion_research/HGSFusion/data
  export CUDA_HOME=/usr/local/cuda-11.7
  export PATH=/usr/local/cuda-11.7/bin:$PATH
  export LD_LIBRARY_PATH=$CONDA_PREFIX/lib:$CONDA_PREFIX/lib/python3.9/site-packages/torch/lib:/usr/local/cuda-11.7/lib64:/usr/lib/wsl/lib:${LD_LIBRARY_PATH:-}
  hash -r
  which python
  python --version
  python - <<'PY' ... torch/mmcv/mmengine/mmdet diagnostics ... PY
  which nvcc
  nvcc --version
  nvidia-smi || true
  git log --oneline -8
  find reproduction -maxdepth 3 -type f | sort
  find reproduction/stage4 -maxdepth 3 -type f | sort
  git diff -- README.md README_UPSTREAM.md reproduction/stage0 reproduction/stage1 reproduction/stage2 reproduction/stage3
  ```
- exit status: `0`
- important output excerpt:
  - python: `/home/user/miniforge3/envs/hgsfusion_a17/bin/python`
  - python version: `3.9.23`
  - `torch 1.13.1+cu117`, `torch.cuda.is_available=True`, `torch.cuda.device_count=1`
  - `mmcv 2.1.0`, `mmengine 0.10.7`, `mmdet 3.3.0`
  - `nvcc` from `/usr/local/cuda-11.7/bin/nvcc` (release 11.7)
  - protected paths diff remained empty.
- files changed:
  - `reproduction/stage4/stage4_execution_log.md`
  - `reproduction/stage4/stage4_reproduction_notes.md`
- reason: Stage 4A baseline environment and protected-path preflight logging.
- next action or blocker: implement Stage 4 scripts/local cfgs and run Stage 4B/4C commands.

### 2026-05-14T17:01:21+08:00
- current branch: `hgsfusion-stage4-training-chain-validation`
- working directory: `/home/user/HGSFusion_research/HGSFusion`
- command block executed:
  ```bash
  # create scripts
  create reproduction/stage4/scripts/stage4_train_data_contract_check.py
  create reproduction/stage4/scripts/stage4_make_info_subset.py
  create reproduction/stage4/scripts/stage4_train_log_parser.py
  create reproduction/stage4/scripts/stage4_train_artifact_check.py
  create reproduction/stage4/scripts/stage4_runtime_summary.py

  # create local cfg copies
  cp tools/cfgs/hgsfusion/hgsfusion_vod.yaml reproduction/stage4/local_cfgs/hgsfusion_vod_stage4_train20.yaml
  cp tools/cfgs/hgsfusion/hgsfusion_tj4d.yaml reproduction/stage4/local_cfgs/hgsfusion_tj4d_stage4_train20.yaml
  cp tools/cfgs/hgsfusion/hgsfusion_vod.yaml reproduction/stage4/local_cfgs/hgsfusion_vod_stage4_train80_ddp.yaml

  # edit only INFO_PATH and NUM_EPOCHS in local cfgs
  diff -u tools/cfgs/hgsfusion/hgsfusion_vod.yaml reproduction/stage4/local_cfgs/hgsfusion_vod_stage4_train20.yaml
  diff -u tools/cfgs/hgsfusion/hgsfusion_tj4d.yaml reproduction/stage4/local_cfgs/hgsfusion_tj4d_stage4_train20.yaml
  diff -u tools/cfgs/hgsfusion/hgsfusion_vod.yaml reproduction/stage4/local_cfgs/hgsfusion_vod_stage4_train80_ddp.yaml
  ```
- exit status: `0`
- important output excerpt:
  - local cfg diffs were minimal:
    - added `DATA_CONFIG.INFO_PATH` train/test subset pkl override
    - set `OPTIMIZATION.NUM_EPOCHS` to `1`
- files changed:
  - `reproduction/stage4/scripts/*.py` (5 files)
  - `reproduction/stage4/local_cfgs/*.yaml` (3 files)
  - `reproduction/stage4/stage4_execution_log.md`
  - `reproduction/stage4/stage4_reproduction_notes.md`
- reason: prepare Stage 4B/4C tooling and bounded local cfgs.
- next action or blocker: run training data contract checks and subset generation.

### 2026-05-14T17:01:21+08:00
- current branch: `hgsfusion-stage4-training-chain-validation`
- working directory: `/home/user/HGSFusion_research/HGSFusion`
- command block executed:
  ```bash
  python reproduction/stage4/scripts/stage4_train_data_contract_check.py --dataset vod --batch-size 1 --workers 0 --max-batches 2
  python reproduction/stage4/scripts/stage4_train_data_contract_check.py --dataset tj4d --batch-size 1 --workers 0 --max-batches 2
  python reproduction/stage4/scripts/stage4_make_info_subset.py --dataset vod  --source data/vod_radar_5frames/kitti_infos_train.pkl --output data/vod_radar_5frames/kitti_infos_stage4_vod_train20.pkl --count 20
  python reproduction/stage4/scripts/stage4_make_info_subset.py --dataset vod  --source data/vod_radar_5frames/kitti_infos_train.pkl --output data/vod_radar_5frames/kitti_infos_stage4_vod_train80.pkl --count 80
  python reproduction/stage4/scripts/stage4_make_info_subset.py --dataset vod  --source data/vod_radar_5frames/kitti_infos_val.pkl   --output data/vod_radar_5frames/kitti_infos_stage4_vod_eval20.pkl --count 20
  python reproduction/stage4/scripts/stage4_make_info_subset.py --dataset tj4d --source data/tj4d/kitti_infos_train.pkl            --output data/tj4d/kitti_infos_stage4_tj4d_train20.pkl --count 20
  python reproduction/stage4/scripts/stage4_make_info_subset.py --dataset tj4d --source data/tj4d/kitti_infos_val.pkl              --output data/tj4d/kitti_infos_stage4_tj4d_eval20.pkl --count 20
  ```
- exit status: `0`
- important output excerpt:
  - `TRAIN_DATA_CONTRACT_OK dataset=vod batches_checked=2`
  - `TRAIN_DATA_CONTRACT_OK dataset=tj4d batches_checked=2`
  - generated subset pkl lengths:
    - VoD train20/train80/eval20 => `20/80/20`
    - TJ4D train20/eval20 => `20/20`
- files changed:
  - runtime-only subset pkl artifacts under `data/` (untracked)
  - `reproduction/stage4/stage4_execution_log.md`
  - `reproduction/stage4/stage4_reproduction_notes.md`
- reason: Stage 4B pass and Stage 4C subset preparation.
- next action or blocker: run VoD bounded training smoke and parse results.

### 2026-05-14T17:01:21+08:00
- current branch: `hgsfusion-stage4-training-chain-validation`
- working directory: `/home/user/HGSFusion_research/HGSFusion`
- command block executed:
  ```bash
  CUDA_VISIBLE_DEVICES=0 python tools/train.py \
    --cfg_file reproduction/stage4/local_cfgs/hgsfusion_vod_stage4_train20.yaml \
    --batch_size 1 --workers 2 --epochs 1 \
    --extra_tag stage4_vod_train20_e1_sg \
    --fix_random_seed --ckpt_save_interval 1 --max_ckpt_save_num 2

  python reproduction/stage4/scripts/stage4_train_log_parser.py \
    --output-dir output/stage4/local_cfgs/hgsfusion_vod_stage4_train20/stage4_vod_train20_e1_sg

  # first artifact check attempt
  python reproduction/stage4/scripts/stage4_train_artifact_check.py \
    --eval-output-dir output/stage4/local_cfgs/hgsfusion_vod_stage4_train20/stage4_vod_train20_e1_sg/eval/eval_with_train/epoch_1/val \
    --expected-count 20
  ```
- exit status: `1` (artifact checker first attempt), training command itself exited `0`
- important output excerpt:
  - training/eval completed for tag `stage4_vod_train20_e1_sg`.
  - finite loss logs observed (`3.569`, `2.860`).
  - checkpoint saved: `.../ckpt/checkpoint_epoch_1.pth`.
  - `stage4_train_log_parser.py` summary:
    - `train_started=True`, `train_ended=True`, `nan_or_inf_loss=False`.
  - artifact checker failure traceback:
    - `TypeError: '<' not supported between instances of 'slice' and 'int'`
    - location: `stage4_train_artifact_check.py`, slicing `Path.parents`.
- files changed:
  - runtime artifacts in `output/stage4/local_cfgs/hgsfusion_vod_stage4_train20/stage4_vod_train20_e1_sg/`
  - `reproduction/stage4/stage4_execution_log.md`
  - `reproduction/stage4/stage4_reproduction_notes.md`
- reason: execute Stage 4C and detect script-side checker bug.
- next action or blocker: patch checker compatibility bug and rerun artifact check.

### 2026-05-14T17:01:21+08:00
- current branch: `hgsfusion-stage4-training-chain-validation`
- working directory: `/home/user/HGSFusion_research/HGSFusion`
- command block executed:
  ```bash
  # fix checker fallback path handling
  patch reproduction/stage4/scripts/stage4_train_artifact_check.py
  python reproduction/stage4/scripts/stage4_train_artifact_check.py \
    --eval-output-dir output/stage4/local_cfgs/hgsfusion_vod_stage4_train20/stage4_vod_train20_e1_sg/eval/eval_with_train/epoch_1/val \
    --expected-count 20

  CUDA_VISIBLE_DEVICES=0 python tools/train.py \
    --cfg_file reproduction/stage4/local_cfgs/hgsfusion_vod_stage4_train20.yaml \
    --batch_size 1 --workers 2 --epochs 2 \
    --ckpt output/stage4/local_cfgs/hgsfusion_vod_stage4_train20/stage4_vod_train20_e1_sg/ckpt/checkpoint_epoch_1.pth \
    --extra_tag stage4_vod_train20_resume_e2_sg \
    --fix_random_seed --ckpt_save_interval 1 --max_ckpt_save_num 2

  python reproduction/stage4/scripts/stage4_train_log_parser.py \
    --output-dir output/stage4/local_cfgs/hgsfusion_vod_stage4_train20/stage4_vod_train20_resume_e2_sg

  python reproduction/stage4/scripts/stage4_train_artifact_check.py \
    --eval-output-dir output/stage4/local_cfgs/hgsfusion_vod_stage4_train20/stage4_vod_train20_resume_e2_sg/eval/eval_with_train/epoch_2/val \
    --expected-count 20
  ```
- exit status: `0`
- important output excerpt:
  - artifact checker pass for VoD epoch1:
    - `TRAIN_AFTER_EVAL_ARTIFACT_CHECK_OK expected=20 actual=20`
  - resume run loaded ckpt and continued from epoch 2.
  - resume run completed with finite losses (`2.112`, `2.124`).
  - epoch2 artifact check pass:
    - `TRAIN_AFTER_EVAL_ARTIFACT_CHECK_OK expected=20 actual=20`
- files changed:
  - `reproduction/stage4/scripts/stage4_train_artifact_check.py`
  - runtime artifacts for `stage4_vod_train20_resume_e2_sg`
  - `reproduction/stage4/stage4_execution_log.md`
  - `reproduction/stage4/stage4_reproduction_notes.md`
- reason: close Stage 4D + Stage 4E for VoD.
- next action or blocker: run hardware gate for Stage 4F and then TJ4D bounded training smoke.

### 2026-05-14T17:01:21+08:00
- current branch: `hgsfusion-stage4-training-chain-validation`
- working directory: `/home/user/HGSFusion_research/HGSFusion`
- command block executed:
  ```bash
  python - <<'PY'
  import torch
  print('cuda_available:', torch.cuda.is_available())
  print('device_count:', torch.cuda.device_count())
  for i in range(torch.cuda.device_count()):
      print(i, torch.cuda.get_device_name(i))
  PY

  CUDA_VISIBLE_DEVICES=0 python tools/train.py \
    --cfg_file reproduction/stage4/local_cfgs/hgsfusion_tj4d_stage4_train20.yaml \
    --batch_size 1 --workers 2 --epochs 1 \
    --extra_tag stage4_tj4d_train20_e1_sg \
    --fix_random_seed --ckpt_save_interval 1 --max_ckpt_save_num 2
  ```
- exit status: `1` (TJ4D run), hardware check exited `0`
- important output excerpt:
  - GPU count check:
    - `cuda_available: True`
    - `device_count: 1`
  - DDP+SyncBN smoke skipped due `<2 GPUs`.
  - TJ4D run trained and evaluated, but failed after eval with traceback:
    - `NotImplementedError: Got <class 'dict'>, but expected numpy array or torch tensor.`
    - source: `tools/test.py` -> `repeat_eval_ckpt` -> `tb_log.add_scalar`.
- files changed:
  - runtime artifacts for failed TJ4D run under `.../stage4_tj4d_train20_e1_sg/`
  - `reproduction/stage4/stage4_execution_log.md`
  - `reproduction/stage4/stage4_reproduction_notes.md`
- reason: Stage 4G failure diagnosis before blocker fix.
- next action or blocker: apply minimal fix in `tools/test.py` to skip non-scalar TensorBoard entries and rerun TJ4D.

### 2026-05-14T17:01:21+08:00
- current branch: `hgsfusion-stage4-training-chain-validation`
- working directory: `/home/user/HGSFusion_research/HGSFusion`
- command block executed:
  ```bash
  # minimal blocker fix
  patch tools/test.py  # only tb_log.add_scalar path in repeat_eval_ckpt

  CUDA_VISIBLE_DEVICES=0 python tools/train.py \
    --cfg_file reproduction/stage4/local_cfgs/hgsfusion_tj4d_stage4_train20.yaml \
    --batch_size 1 --workers 2 --epochs 1 \
    --extra_tag stage4_tj4d_train20_e1_sg_fix1 \
    --fix_random_seed --ckpt_save_interval 1 --max_ckpt_save_num 2

  python reproduction/stage4/scripts/stage4_train_log_parser.py \
    --output-dir output/stage4/local_cfgs/hgsfusion_tj4d_stage4_train20/stage4_tj4d_train20_e1_sg_fix1

  python reproduction/stage4/scripts/stage4_train_artifact_check.py \
    --eval-output-dir output/stage4/local_cfgs/hgsfusion_tj4d_stage4_train20/stage4_tj4d_train20_e1_sg_fix1/eval/eval_with_train/epoch_1/val \
    --expected-count 20

  python reproduction/stage4/scripts/stage4_runtime_summary.py

  git branch --show-current
  git status --short
  git diff -- README.md README_UPSTREAM.md reproduction/stage0 reproduction/stage1 reproduction/stage2 reproduction/stage3
  git diff --name-only
  find . -path './output' -prune -o -path './data' -prune -o -name '__pycache__' -print
  find . -path './output' -prune -o -path './data' -prune -o -name '*.pyc' -print
  find . -path './output' -prune -o -path './data' -prune -o -name 'result.pkl' -print
  find . -path './output' -prune -o -path './data' -prune -o -name 'final_result' -print
  find . -path './output' -prune -o -path './data' -prune -o -name '*.pth' -print
  ```
- exit status: `0`
- important output excerpt:
  - TJ4D rerun completed end-to-end.
  - warning logs from fix:
    - `Skip non-scalar tb metric: dark|standard|shiny|all_weather (type=dict)`
  - TJ4D artifact checker pass:
    - `TRAIN_AFTER_EVAL_ARTIFACT_CHECK_OK expected=20 actual=20`
  - runtime summary generated:
    - `reproduction/stage4/outputs/stage4_training_summary.json`
    - `reproduction/stage4/outputs/stage4_training_summary.csv`
  - final hygiene checks:
    - protected paths diff is empty.
    - branch remains `hgsfusion-stage4-training-chain-validation`.
- files changed:
  - `tools/test.py`
  - `reproduction/stage4/scripts/*`
  - `reproduction/stage4/local_cfgs/*`
  - `reproduction/stage4/outputs/stage4_training_summary.json`
  - `reproduction/stage4/outputs/stage4_training_summary.csv`
  - `reproduction/stage4/stage4_execution_log.md`
  - `reproduction/stage4/stage4_reproduction_notes.md`
- reason: close Stage 4G with blocker fix and perform runtime summary/final hygiene checks.
- next action or blocker: stage allowed files and create incremental Stage 4 commits.

### 2026-05-14T17:04:15+08:00
- current branch: `hgsfusion-stage4-training-chain-validation`
- working directory: `/home/user/HGSFusion_research/HGSFusion`
- command block executed:
  ```bash
  git status --short
  git diff -- README.md
  git add reproduction/stage4/stage4_execution_log.md reproduction/stage4/stage4_reproduction_notes.md \
          reproduction/stage4/scripts/stage4_train_data_contract_check.py \
          reproduction/stage4/scripts/stage4_make_info_subset.py \
          reproduction/stage4/scripts/stage4_train_log_parser.py \
          reproduction/stage4/scripts/stage4_train_artifact_check.py \
          reproduction/stage4/scripts/stage4_runtime_summary.py \
          reproduction/stage4/local_cfgs/hgsfusion_vod_stage4_train20.yaml \
          reproduction/stage4/local_cfgs/hgsfusion_tj4d_stage4_train20.yaml \
          reproduction/stage4/local_cfgs/hgsfusion_vod_stage4_train80_ddp.yaml \
          reproduction/stage4/outputs/stage4_training_summary.json \
          reproduction/stage4/outputs/stage4_training_summary.csv \
          tools/test.py
  git commit -m "stage4: run bounded training-chain validation and blocker fix"
  git rev-parse --short HEAD
  ```
- exit status: `0`
- important output excerpt:
  - `git diff -- README.md` empty before commit.
  - created commit hash: `1223b0e`
  - commit message: `stage4: run bounded training-chain validation and blocker fix`
- files changed:
  - `reproduction/stage4/` scripts/local cfgs/outputs/docs
  - `tools/test.py` (minimal non-scalar TensorBoard guard in `repeat_eval_ckpt`)
- reason: record Stage 4 implementation and validation changes in one coherent commit.
- next action or blocker: commit final execution-log hash record.
