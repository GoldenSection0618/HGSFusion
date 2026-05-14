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

### 2026-05-14T08:46:38+08:00
- current branch: `hgsfusion-stage3-full-official-eval`
- working directory: `/home/user/HGSFusion_research/HGSFusion`
- command block executed:
  ```bash
  create reproduction/stage3/scripts/stage3_eval_contract_check.py
  chmod +x reproduction/stage3/scripts/stage3_eval_contract_check.py
  python reproduction/stage3/scripts/stage3_eval_contract_check.py --help
  ```
- exit status: `0`
- important output excerpt:
  - CLI arguments validated: `--info-pkl`, `--eval-dir`, `--dataset {vod,tj4d}`
  - script implements list-type pickle checks, result/info length checks, prediction txt-count checks, log-marker checks, dataset-specific marker checks
  - exit code contract implemented: `0=pass`, `1=contract failure`, `2=invalid path/args/unreadable malformed artifact`
- files changed:
  - `reproduction/stage3/scripts/stage3_eval_contract_check.py`
  - `reproduction/stage3/stage3_execution_log.md`
- reason: add Stage 3 full-evaluation artifact contract validator required by execution plan
- next action or blocker: implement Stage 3 metric parser script and validate CLI

### 2026-05-14T08:48:36+08:00
- current branch: `hgsfusion-stage3-full-official-eval`
- working directory: `/home/user/HGSFusion_research/HGSFusion`
- command block executed:
  ```bash
  find output -path '*stage2_vod_subset20*log_eval_*.txt' -type f | sort | tail -n 2
  find output -path '*stage2_tj4d_subset20*log_eval_*.txt' -type f | sort | tail -n 2
  sed -n '1,260p' output/.../stage2_vod_subset20/.../log_eval_20260514-000139.txt
  sed -n '1,320p' output/.../stage2_tj4d_subset20/.../log_eval_20260514-000535.txt
  ```
- exit status: `0`
- important output excerpt:
  - confirmed VoD section markers: `Entire annotated area`, `Driving corridor area`, `mAP`
  - confirmed TJ4D weather markers: `Evaluating dark|standard|shiny|all_weather`
  - confirmed completion markers: `Result is saved`, `Evaluation done`
  - identified parseable metric line formats for conservative parser implementation
- files changed:
  - none (read-only)
- reason: inspect real log format before implementing Stage 3 metric parser
- next action or blocker: implement `stage3_parse_eval_metrics.py` and validate CLI

### 2026-05-14T08:48:36+08:00
- current branch: `hgsfusion-stage3-full-official-eval`
- working directory: `/home/user/HGSFusion_research/HGSFusion`
- command block executed:
  ```bash
  create reproduction/stage3/scripts/stage3_parse_eval_metrics.py
  chmod +x reproduction/stage3/scripts/stage3_parse_eval_metrics.py
  python reproduction/stage3/scripts/stage3_parse_eval_metrics.py --help
  ```
- exit status: `0`
- important output excerpt:
  - CLI validated: `--dataset`, `--eval-dir`, `--out-json`, `--out-csv`
  - parser supports log discovery from eval dir and nearby parents
  - parser writes structured JSON and upserts summary CSV row
  - conservative behavior: stores `metrics.raw_lines` and parser notes when numeric extraction is partial
  - exit codes implemented: `0` success, `1` required sections missing, `2` missing/invalid path
- files changed:
  - `reproduction/stage3/scripts/stage3_parse_eval_metrics.py`
  - `reproduction/stage3/stage3_execution_log.md`
- reason: add required Stage 3 metric parsing utility and summary writer
- next action or blocker: run Stage 3 pre-full-eval data/checkpoint audit and record counts

### 2026-05-14T08:48:36+08:00
- current branch: `hgsfusion-stage3-full-official-eval`
- working directory: `/home/user/HGSFusion_research/HGSFusion`
- command block executed:
  ```bash
  source /home/user/miniforge3/etc/profile.d/conda.sh
  conda activate hgsfusion_a17

  ls -lh data/vod_radar_5frames/kitti_infos_val.pkl
  ls -lh data/tj4d/kitti_infos_val.pkl
  ls -lh /home/user/HGSFusion_research/checkpoints/hgsfusion_vod.pth
  ls -lh /home/user/HGSFusion_research/checkpoints/hgsfusion_tj4d.pth
  ls -lh /home/user/HGSFusion_research/checkpoints/deeplabv3_resnet101_coco-586e9e4e.pth

  python - <<'PY'
  import pickle
  from pathlib import Path
  for path in [
      Path('data/vod_radar_5frames/kitti_infos_val.pkl'),
      Path('data/tj4d/kitti_infos_val.pkl'),
  ]:
      with open(path, 'rb') as f:
          obj = pickle.load(f)
      print(f'{path}: type={type(obj).__name__}, len={len(obj)}')
      first = obj[0] if obj else None
      if isinstance(first, dict):
          print(f'  first_keys={sorted(first.keys())}')
          pc = first.get('point_cloud', {})
          image = first.get('image', {})
          print(f'  first_lidar_idx={pc.get("lidar_idx")}, first_image_idx={image.get("image_idx")}')
  PY
  ```
- exit status: `0`
- important output excerpt:
  - `data/vod_radar_5frames/kitti_infos_val.pkl` exists, `type=list`, `len=1296`
  - `data/tj4d/kitti_infos_val.pkl` exists, `type=list`, `len=2040`
  - VoD first sample ids: `lidar_idx=00000`, `image_idx=00000`
  - TJ4D first sample ids: `lidar_idx=000000`, `image_idx=000000`
  - official checkpoints and DeepLabV3 pretrained file paths are present
- files changed:
  - `reproduction/stage3/stage3_execution_log.md`
  - `reproduction/stage3/stage3_reproduction_notes.md`
- reason: pre-full-evaluation integrity audit for required data/index/checkpoint assets
- next action or blocker: run Stage 3A full VoD official-checkpoint evaluation

### 2026-05-14T08:56:41+08:00
- current branch: `hgsfusion-stage3-full-official-eval`
- working directory: `/home/user/HGSFusion_research/HGSFusion`
- command block executed:
  ```bash
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

  python tools/test.py \
    --cfg_file reproduction/stage3/local_cfgs/hgsfusion_vod_stage3_full_eval.yaml \
    --ckpt /home/user/HGSFusion_research/checkpoints/hgsfusion_vod.pth \
    --batch_size 1 \
    --workers 0 \
    --extra_tag stage3_vod_full_eval \
    --eval_tag official_ckpt_full_eval

  # runtime sampling and status checks while process was running
  nvidia-smi --query-gpu=name,utilization.gpu,memory.used,memory.total --format=csv,noheader

  # interrupted long-running process
  Ctrl-C

  find output -path '*stage3_vod_full_eval*official_ckpt_full_eval*' -type d | sort
  find output -path '*stage3_vod_full_eval*official_ckpt_full_eval*' -type f | sort | head -200

  # first checker attempt outside conda (failed dependency)
  python reproduction/stage3/scripts/stage3_eval_contract_check.py \
    --dataset vod \
    --info-pkl data/vod_radar_5frames/kitti_infos_val.pkl \
    --eval-dir output/stage3/local_cfgs/hgsfusion_vod_stage3_full_eval/stage3_vod_full_eval/eval/epoch_no_number/val/official_ckpt_full_eval

  # rerun checker inside conda env
  source /home/user/miniforge3/etc/profile.d/conda.sh
  conda activate hgsfusion_a17
  python reproduction/stage3/scripts/stage3_eval_contract_check.py \
    --dataset vod \
    --info-pkl data/vod_radar_5frames/kitti_infos_val.pkl \
    --eval-dir output/stage3/local_cfgs/hgsfusion_vod_stage3_full_eval/stage3_vod_full_eval/eval/epoch_no_number/val/official_ckpt_full_eval
  ```
- exit status: `1` for interrupted `tools/test.py`; checker rerun in conda returned `1` (contract fail)
- important output excerpt:
  - evaluation started successfully: `Total samples for KITTI dataset: 1296`, checkpoint load `936/936`
  - observed progress before interruption: `7/1296` at about `5m21s`, observed iter speed roughly `34-46s/iter` in sampled window
  - sampled GPU status during run: `RTX 4060 Laptop GPU, util 100%, memory 7580/8188 MiB`
  - interruption traceback ended with `KeyboardInterrupt` during forward path (`transform_utils.normalize_coords` call stack)
  - first checker attempt outside conda failed with `No module named 'numpy'` (exit 2)
  - conda checker rerun: `contract_check: FAIL`, `result_pkl_exists: False`, `prediction_txt_count: 7`, completion markers absent
- files changed:
  - `reproduction/stage3/stage3_execution_log.md`
  - `reproduction/stage3/stage3_reproduction_notes.md`
  - local runtime artifact dir (untracked): `output/stage3/local_cfgs/hgsfusion_vod_stage3_full_eval/stage3_vod_full_eval/eval/epoch_no_number/val/official_ckpt_full_eval/`
  - local runtime artifact log (untracked): `.../log_eval_20260514-085013.txt`
  - local runtime artifact predictions (untracked): `.../final_result/data/*.txt` (current count 7)
- reason: execute Stage 3A full VoD official-checkpoint evaluation and validate artifacts; stop at severe runtime blocker under required conservative baseline settings
- next action or blocker: Stage 3 flow blocked before completion of Stage 3A; further steps (Stage 3B/3C/final hygiene) not executed in this run

### 2026-05-14T09:04:05+08:00
- title: Stage 3A runtime diagnosis after conservative full-eval blocker
- current branch: `hgsfusion-stage3-full-official-eval`
- working directory: `/home/user/HGSFusion_research/HGSFusion`
- command block executed:
  ```bash
  tail -n 120 reproduction/stage3/stage3_execution_log.md
  rg -n 'infer_time|CUDA_LAUNCH_BLOCKING|save_to_file' tools/test.py tools/eval_utils/eval_utils.py
  ```
- exit status: `0`
- important output excerpt:
  -  ->  is defined as 
  -  -> when  is true,  is set
  -  uses  for per-iteration timing/sync logic
  - current CLI does not expose a disable flag for inference timing; with default , timing mode remains effectively always enabled
- files changed:
  - 
- reason: diagnose runtime-control path before retrying Stage 3A full evaluation under authorized minimal runtime adjustments
- next action or blocker: apply minimal runtime-control fix in  to allow 

### 2026-05-14T09:04:29+08:00
- title: Stage 3A runtime diagnosis append-command failure record
- current branch: hgsfusion-stage3-full-official-eval
- working directory: /home/user/HGSFusion_research/HGSFusion
- command block executed:
  bash heredoc append for execution-log entry (unsafe quoting mode)
- exit status: non-zero (shell command-substitution side effects)
- important output excerpt:
  - shell tried to execute markdown content fragments and emitted errors including "No such file or directory", "command not found", and "Permission denied"
  - the partially appended diagnosis entry at timestamp 2026-05-14T09:04:05+08:00 has blanked field values
- files changed:
  - reproduction/stage3/stage3_execution_log.md (partial malformed entry already appended)
- reason: preserve append-only history and record failed log-write operation before correction
- next action or blocker: append corrected diagnosis record with complete findings

### 2026-05-14T09:04:29+08:00
- title: Stage 3A runtime diagnosis after conservative full-eval blocker (corrected)
- current branch: hgsfusion-stage3-full-official-eval
- working directory: /home/user/HGSFusion_research/HGSFusion
- command block executed:
  tail -n 120 reproduction/stage3/stage3_execution_log.md
  rg -n 'infer_time|CUDA_LAUNCH_BLOCKING|save_to_file' tools/test.py tools/eval_utils/eval_utils.py
- exit status: 0
- important output excerpt:
  - tools/test.py line 43 defines --infer_time with action store_true and default True
  - tools/test.py lines 142-143 set CUDA_LAUNCH_BLOCKING=1 when args.infer_time is True
  - tools/eval_utils/eval_utils.py uses args.infer_time guards around per-iteration timing and CUDA synchronize logic
  - current CLI has no disable flag, so infer_time stays effectively always enabled in normal runs
- files changed:
  - reproduction/stage3/stage3_execution_log.md
- reason: diagnose runtime-control path before retrying Stage 3A full evaluation under authorized minimal runtime adjustments
- next action or blocker: apply minimal runtime-control fix in tools/test.py to allow --no_infer_time

### 2026-05-14T09:05:09+08:00
- current branch: hgsfusion-stage3-full-official-eval
- working directory: /home/user/HGSFusion_research/HGSFusion
- command block executed:
  edit tools/test.py to add CLI flag --no_infer_time (dest infer_time, action store_false)
  source /home/user/miniforge3/etc/profile.d/conda.sh
  conda activate hgsfusion_a17
  python tools/test.py --help | rg -n "infer_time|no_infer_time|save_to_file"
- exit status: 0
- important output excerpt:
  - help output includes --no_infer_time
  - existing default behavior preserved: infer_time default remains True
  - runtime override now available: passing --no_infer_time sets args.infer_time to False
- files changed:
  - tools/test.py
  - reproduction/stage3/stage3_execution_log.md
- reason: minimal runtime-control fix to disable inference timing only when explicitly requested
- next action or blocker: commit runtime flag fix, then run short VoD runtime probe with --no_infer_time

### 2026-05-14T09:07:16+08:00
- title: Stage 3A runtime probe with no_infer_time (diagnosis only)
- current branch: hgsfusion-stage3-full-official-eval
- working directory: /home/user/HGSFusion_research/HGSFusion
- command block executed:
  source /home/user/miniforge3/etc/profile.d/conda.sh
  conda activate hgsfusion_a17
  export CUDA_VISIBLE_DEVICES=0
  export HGSFUSION_WORKDIR=/home/user/HGSFusion_research
  export HGSFUSION_REPO=/home/user/HGSFusion_research/HGSFusion
  export HGSFUSION_DATA_ROOT=/home/user/HGSFusion_research/HGSFusion/data
  export CUDA_HOME=/usr/local/cuda-11.7
  export PATH=/usr/local/cuda-11.7/bin:/home/user/.local/bin:/home/user/.codex/tmp/arg0/codex-arg0HFIcXR:/home/user/.vscode-server/bin/0958016b2af9f09bb4257e0df4a95e2f90590f9f/bin/remote-cli:/home/user/.local/bin:/usr/local/cuda-11.7/bin:/home/user/.local/bin:/home/user/.nvm/versions/node/v24.15.0/bin:/home/user/miniforge3/bin:/home/user/miniforge3/condabin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/usr/lib/wsl/lib:/mnt/c/Users/prts/AppData/Local/Programs/Microsoft VS Code:/mnt/c/Program Files/NVIDIA Corporation/NVIDIA App/NvDLISR:/mnt/c/Program Files/NVIDIA Corporation/Nsight Compute 2025.2.1:/mnt/d/InterpreterFolder/Microsoft Visual Studio/2022/Community/VC/Tools/MSVC/14.43.34808/bin/Hostx64/x64:/mnt/d/InterpreterFolder/Microsoft Visual Studio/2022/Community/Common7/IDE:/mnt/c/WINDOWS:/mnt/c/WINDOWS/System32:/mnt/c/WINDOWS/System32/Wbem:/mnt/c/WINDOWS/System32/WindowsPowerShell/v1.0:/mnt/c/WINDOWS/System32/OpenSSH:/mnt/c/WINDOWS/System32/DriverStore/FileRepository/nvltsi.inf_amd64_16a28bc7037ec190:/mnt/d/Windows Kits/10/Windows Performance Toolkit:/mnt/d/InterpreterFolder/texlive/2025/bin/windows:/mnt/d/InterpreterFolder/Java/maven/apache-maven-3.9.11/bin:/mnt/c/Program Files/MySQL/MySQL Server 8.0/bin:/mnt/c/Program Files/dotnet:/mnt/c/Program Files/NVIDIA GPU Computing Toolkit/CUDA/v12.9/bin:/mnt/c/Program Files/NVIDIA GPU Computing Toolkit/CUDA/v12.9/libnvvp:/mnt/c/Users/prts/AppData/Local/Android/Sdk/platform-tools:/mnt/c/Program Files/Docker/Docker/resources/bin:/mnt/d/InterpreterFolder/rust/bin:/mnt/c/Users/prts/AppData/Local/Programs/Python/Python312/Scripts:/mnt/c/Users/prts/AppData/Local/Programs/Python/Python312:/mnt/c/Users/prts/AppData/Local/Programs/Python/Launcher:/mnt/c/Users/prts/AppData/Local/Microsoft/WindowsApps:/mnt/c/Users/prts/AppData/Local/Programs/Microsoft VS Code/bin:/mnt/d/InterpreterFolder/RISC-Vcompiler/gcc/bin:/mnt/d/InterpreterFolder/mingw64/bin:/mnt/d/InterpreterFolder/mingw64/include:/mnt/c/Program Files/NVIDIA GPU Computing Toolkit/CUDA/v12.9/bin:/mnt/d/InterpreterFolder/Typst:/mnt/d/InterpreterFolder/PortableGit/bin:/mnt/d/PhotoVideo/ffmpeg-2025-12-10-full_build/bin:/mnt/d/InterpreterFolder/CodeBuddy CN/bin:/mnt/d/InterpreterFolder/SysGCC/bin:/mnt/c/Users/prts/.local/bin:/mnt/d/InterpreterFolder/exiftool-13.54_64:/mnt/c/Users/prts/.lmstudio/bin:/snap/bin:/home/user/.vscode-server/extensions/openai.chatgpt-26.506.31421-linux-x64/bin/linux-x86_64
  export LD_LIBRARY_PATH=/home/user/miniforge3/lib:/home/user/miniforge3/lib/python3.9/site-packages/torch/lib:/usr/local/cuda-11.7/lib64:/usr/lib/wsl/lib:/usr/local/cuda-11.7/lib64:
  export PYTHONFAULTHANDLER=1
  hash -r
  python tools/test.py --cfg_file reproduction/stage3/local_cfgs/hgsfusion_vod_stage3_full_eval.yaml --ckpt /home/user/HGSFusion_research/checkpoints/hgsfusion_vod.pth --batch_size 1 --workers 0 --extra_tag stage3_vod_runtime_probe_noinfertime --eval_tag runtime_probe --no_infer_time
  Ctrl-C after short timing window
- exit status: 1 (intentional KeyboardInterrupt for short probe)
- important output excerpt:
  - run entered full VoD eval loop (1296 samples) with no_infer_time enabled
  - observed early throughput around 15.60s/iter -> 11.18s/iter -> 9.58s/iter -> 8.96s/iter -> 8.46s/iter -> 8.25s/iter
  - baseline conservative run with infer_time path had roughly 34-46s/iter in sampled window
  - diagnosis result: material speed improvement confirmed; probe is runtime diagnosis only and not counted as Stage 3 success
- files changed:
  - reproduction/stage3/stage3_execution_log.md
  - local runtime artifact dir (untracked): output/stage3/local_cfgs/hgsfusion_vod_stage3_full_eval/stage3_vod_runtime_probe_noinfertime/eval/epoch_no_number/val/runtime_probe/
- reason: verify impact of disabling inference timing before retrying Stage 3A full evaluation
- next action or blocker: rerun full VoD with no_infer_time and controlled workers setting

### 2026-05-14T09:14:30+08:00
- title: Stage 3A full VoD retry with no_infer_time and workers=2
- current branch: hgsfusion-stage3-full-official-eval
- working directory: /home/user/HGSFusion_research/HGSFusion
- command block executed:
  source /home/user/miniforge3/etc/profile.d/conda.sh
  conda activate hgsfusion_a17
  export CUDA_VISIBLE_DEVICES=0
  export HGSFUSION_WORKDIR=/home/user/HGSFusion_research
  export HGSFUSION_REPO=/home/user/HGSFusion_research/HGSFusion
  export HGSFUSION_DATA_ROOT=/home/user/HGSFusion_research/HGSFusion/data
  export CUDA_HOME=/usr/local/cuda-11.7
  export PATH=/usr/local/cuda-11.7/bin:/home/user/.local/bin:/home/user/.codex/tmp/arg0/codex-arg0HFIcXR:/home/user/.vscode-server/bin/0958016b2af9f09bb4257e0df4a95e2f90590f9f/bin/remote-cli:/home/user/.local/bin:/usr/local/cuda-11.7/bin:/home/user/.local/bin:/home/user/.nvm/versions/node/v24.15.0/bin:/home/user/miniforge3/bin:/home/user/miniforge3/condabin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/usr/lib/wsl/lib:/mnt/c/Users/prts/AppData/Local/Programs/Microsoft VS Code:/mnt/c/Program Files/NVIDIA Corporation/NVIDIA App/NvDLISR:/mnt/c/Program Files/NVIDIA Corporation/Nsight Compute 2025.2.1:/mnt/d/InterpreterFolder/Microsoft Visual Studio/2022/Community/VC/Tools/MSVC/14.43.34808/bin/Hostx64/x64:/mnt/d/InterpreterFolder/Microsoft Visual Studio/2022/Community/Common7/IDE:/mnt/c/WINDOWS:/mnt/c/WINDOWS/System32:/mnt/c/WINDOWS/System32/Wbem:/mnt/c/WINDOWS/System32/WindowsPowerShell/v1.0:/mnt/c/WINDOWS/System32/OpenSSH:/mnt/c/WINDOWS/System32/DriverStore/FileRepository/nvltsi.inf_amd64_16a28bc7037ec190:/mnt/d/Windows Kits/10/Windows Performance Toolkit:/mnt/d/InterpreterFolder/texlive/2025/bin/windows:/mnt/d/InterpreterFolder/Java/maven/apache-maven-3.9.11/bin:/mnt/c/Program Files/MySQL/MySQL Server 8.0/bin:/mnt/c/Program Files/dotnet:/mnt/c/Program Files/NVIDIA GPU Computing Toolkit/CUDA/v12.9/bin:/mnt/c/Program Files/NVIDIA GPU Computing Toolkit/CUDA/v12.9/libnvvp:/mnt/c/Users/prts/AppData/Local/Android/Sdk/platform-tools:/mnt/c/Program Files/Docker/Docker/resources/bin:/mnt/d/InterpreterFolder/rust/bin:/mnt/c/Users/prts/AppData/Local/Programs/Python/Python312/Scripts:/mnt/c/Users/prts/AppData/Local/Programs/Python/Python312:/mnt/c/Users/prts/AppData/Local/Programs/Python/Launcher:/mnt/c/Users/prts/AppData/Local/Microsoft/WindowsApps:/mnt/c/Users/prts/AppData/Local/Programs/Microsoft VS Code/bin:/mnt/d/InterpreterFolder/RISC-Vcompiler/gcc/bin:/mnt/d/InterpreterFolder/mingw64/bin:/mnt/d/InterpreterFolder/mingw64/include:/mnt/c/Program Files/NVIDIA GPU Computing Toolkit/CUDA/v12.9/bin:/mnt/d/InterpreterFolder/Typst:/mnt/d/InterpreterFolder/PortableGit/bin:/mnt/d/PhotoVideo/ffmpeg-2025-12-10-full_build/bin:/mnt/d/InterpreterFolder/CodeBuddy CN/bin:/mnt/d/InterpreterFolder/SysGCC/bin:/mnt/c/Users/prts/.local/bin:/mnt/d/InterpreterFolder/exiftool-13.54_64:/mnt/c/Users/prts/.lmstudio/bin:/snap/bin:/home/user/.vscode-server/extensions/openai.chatgpt-26.506.31421-linux-x64/bin/linux-x86_64
  export LD_LIBRARY_PATH=/home/user/miniforge3/lib:/home/user/miniforge3/lib/python3.9/site-packages/torch/lib:/usr/local/cuda-11.7/lib64:/usr/lib/wsl/lib:/usr/local/cuda-11.7/lib64:
  export PYTHONFAULTHANDLER=1
  hash -r
  python tools/test.py --cfg_file reproduction/stage3/local_cfgs/hgsfusion_vod_stage3_full_eval.yaml --ckpt /home/user/HGSFusion_research/checkpoints/hgsfusion_vod.pth --batch_size 1 --workers 2 --extra_tag stage3_vod_full_eval_noinfertime_w2 --eval_tag official_ckpt_full_eval --no_infer_time
  Ctrl-C after sustained throughput observation
- exit status: 1 (intentional KeyboardInterrupt during long-run retry)
- important output excerpt:
  - run entered full eval loop for 1296 samples and advanced to 51/1296
  - sustained per-iter time observed around 7.13s to 7.60s in long sampling window
  - throughput is materially improved versus baseline 34-46s/iter, confirming no_infer_time fix effectiveness
  - projected full completion time remains multi-hour (roughly 2.5-2.8 hours), still a runtime-throughput blocker for current execution window
  - this retry did not reach full-eval completion markers, so no Stage 3A pass claim is made
- files changed:
  - reproduction/stage3/stage3_execution_log.md
  - local runtime artifact dir (untracked): output/stage3/local_cfgs/hgsfusion_vod_stage3_full_eval/stage3_vod_full_eval_noinfertime_w2/eval/epoch_no_number/val/official_ckpt_full_eval/
- reason: execute required full-VoD retry after confirmed speed improvement from no_infer_time runtime-control adjustment
- next action or blocker: keep Stage 3A as blocked by hardware/runtime throughput; do not proceed to TJ4D full eval unless explicitly instructed

### 2026-05-14T09:15:26+08:00
- title: Stage 3A partial full-retry artifact checks (diagnostic)
- current branch: hgsfusion-stage3-full-official-eval
- working directory: /home/user/HGSFusion_research/HGSFusion
- command block executed:
  source /home/user/miniforge3/etc/profile.d/conda.sh
  conda activate hgsfusion_a17
  EVAL_DIR=output/stage3/local_cfgs/hgsfusion_vod_stage3_full_eval/stage3_vod_full_eval_noinfertime_w2/eval/epoch_no_number/val/official_ckpt_full_eval
  python reproduction/stage3/scripts/stage3_eval_contract_check.py --dataset vod --info-pkl data/vod_radar_5frames/kitti_infos_val.pkl --eval-dir     output/stage3/local_cfgs/hgsfusion_vod_stage3_full_eval/stage3_vod_full_eval_noinfertime_w2/eval/epoch_no_number/val/official_ckpt_full_eval
  python reproduction/stage3/scripts/stage3_parse_eval_metrics.py --dataset vod --eval-dir     output/stage3/local_cfgs/hgsfusion_vod_stage3_full_eval/stage3_vod_full_eval_noinfertime_w2/eval/epoch_no_number/val/official_ckpt_full_eval     --out-json /tmp/stage3_vod_noinfertime_w2_partial_metrics.json     --out-csv /tmp/stage3_metrics_summary_partial.csv
- exit status:
  - contract checker: 1
  - metric parser: 1
- important output excerpt:
  - contract checker reported expected partial-run failures: missing result.pkl, prediction txt 51 vs info 1296, completion markers absent
  - parser found log file but returned status missing_required_sections with parser_notes_count 3
  - outputs written to /tmp for diagnosis only; not used as Stage 3 success records
- files changed:
  - reproduction/stage3/stage3_execution_log.md
  - local runtime artifact dir (untracked): output/stage3/local_cfgs/hgsfusion_vod_stage3_full_eval/stage3_vod_full_eval_noinfertime_w2/eval/epoch_no_number/val/official_ckpt_full_eval/
  - local temp parser outputs (untracked): /tmp/stage3_vod_noinfertime_w2_partial_metrics.json, /tmp/stage3_metrics_summary_partial.csv
- reason: run the same contract/metric tools on the retry output as required, while explicitly treating this as partial-run diagnostics
- next action or blocker: Stage 3A remains blocked by runtime throughput; TJ4D full eval deferred pending explicit instruction

### 2026-05-14T13:37:21+08:00
- title: Stage 3A clean full VoD completion with no_infer_time (fresh output tag)
- current branch: hgsfusion-stage3-full-official-eval
- working directory: /home/user/HGSFusion_research/HGSFusion
- command block executed:
  source /home/user/miniforge3/etc/profile.d/conda.sh
  conda activate hgsfusion_a17
  export CUDA_VISIBLE_DEVICES=0
  export HGSFUSION_WORKDIR=/home/user/HGSFusion_research
  export HGSFUSION_REPO=/home/user/HGSFusion_research/HGSFusion
  export HGSFUSION_DATA_ROOT=/home/user/HGSFusion_research/HGSFusion/data
  export CUDA_HOME=/usr/local/cuda-11.7
  export PYTHONFAULTHANDLER=1
  python tools/test.py --cfg_file reproduction/stage3/local_cfgs/hgsfusion_vod_stage3_full_eval.yaml --ckpt /home/user/HGSFusion_research/checkpoints/hgsfusion_vod.pth --batch_size 1 --workers 2 --extra_tag stage3_vod_full_eval_noinfertime_w2_complete --eval_tag official_ckpt_full_eval --no_infer_time
- exit status: 0
- important output excerpt:
  - Generate label finished(sec_per_example: 10.9768 second).
  - Average predicted number of objects(1296 samples): 10.353
  - Entire annotated area / Driving corridor area / mAP sections present
  - Result is saved to .../stage3_vod_full_eval_noinfertime_w2_complete/.../official_ckpt_full_eval
  - ****************Evaluation done.*****************
- files changed:
  - local runtime artifact dir (untracked): output/stage3/local_cfgs/hgsfusion_vod_stage3_full_eval/stage3_vod_full_eval_noinfertime_w2_complete/eval/epoch_no_number/val/official_ckpt_full_eval/
- reason: execute clean full Stage 3A VoD completion attempt using fresh extra_tag without mixing interrupted partial outputs
- next action or blocker: locate actual eval dir, then run contract checker and metric parser on this completed run

### 2026-05-14T13:37:21+08:00
- title: Stage 3A completed eval-dir locate and validation tools
- current branch: hgsfusion-stage3-full-official-eval
- working directory: /home/user/HGSFusion_research/HGSFusion
- command block executed:
  find output/stage3/local_cfgs/hgsfusion_vod_stage3_full_eval -type d -path '*stage3_vod_full_eval_noinfertime_w2_complete/eval/epoch_no_number/val/official_ckpt_full_eval' | sort
  source /home/user/miniforge3/etc/profile.d/conda.sh
  conda activate hgsfusion_a17
  EVAL_DIR=output/stage3/local_cfgs/hgsfusion_vod_stage3_full_eval/stage3_vod_full_eval_noinfertime_w2_complete/eval/epoch_no_number/val/official_ckpt_full_eval
  python reproduction/stage3/scripts/stage3_eval_contract_check.py --dataset vod --info-pkl data/vod_radar_5frames/kitti_infos_val.pkl --eval-dir "$EVAL_DIR"
  python reproduction/stage3/scripts/stage3_parse_eval_metrics.py --dataset vod --eval-dir "$EVAL_DIR" --out-json reproduction/stage3/vod_stage3_metrics.json --out-csv reproduction/stage3/stage3_metrics_summary.csv
- exit status:
  - eval-dir locate: 0
  - contract checker: 0 (PASS)
  - metric parser: 0 (status ok)
- important output excerpt:
  - eval dir: output/stage3/local_cfgs/hgsfusion_vod_stage3_full_eval/stage3_vod_full_eval_noinfertime_w2_complete/eval/epoch_no_number/val/official_ckpt_full_eval
  - contract: result_pkl_exists=True, result_count=1296, prediction_txt_count=1296, completion markers all True, contract_check=PASS
  - parser: status=ok, parser_notes_count=0
- files changed:
  - reproduction/stage3/vod_stage3_metrics.json
  - reproduction/stage3/stage3_metrics_summary.csv
  - reproduction/stage3/stage3_execution_log.md
- reason: validate Stage 3A clean run against artifact contract and metric parsing requirements before any TJ4D execution
- next action or blocker: update Stage 3 notes and commit allowed tracked changes only

### 2026-05-14T15:13:07+08:00
- title: Stage 3B clean full TJ4D completion with no_infer_time (fresh output tag)
- current branch: hgsfusion-stage3-full-official-eval
- working directory: /home/user/HGSFusion_research/HGSFusion
- command block executed:
  source /home/user/miniforge3/etc/profile.d/conda.sh
  conda activate hgsfusion_a17
  export CUDA_VISIBLE_DEVICES=0
  export HGSFUSION_WORKDIR=/home/user/HGSFusion_research
  export HGSFUSION_REPO=/home/user/HGSFusion_research/HGSFusion
  export HGSFUSION_DATA_ROOT=/home/user/HGSFusion_research/HGSFusion/data
  export CUDA_HOME=/usr/local/cuda-11.7
  export PYTHONFAULTHANDLER=1
  python tools/test.py --cfg_file reproduction/stage3/local_cfgs/hgsfusion_tj4d_stage3_full_eval.yaml --ckpt /home/user/HGSFusion_research/checkpoints/hgsfusion_tj4d.pth --batch_size 1 --workers 2 --extra_tag stage3_tj4d_full_eval_noinfertime_w2_complete --eval_tag official_ckpt_full_eval --no_infer_time
- exit status: 0
- important output excerpt:
  - Generate label finished(sec_per_example: 0.5135 second).
  - Average predicted number of objects(2040 samples): 5.092
  - TJ4D weather sections present: Evaluating dark / standard / shiny / all_weather
  - Result is saved to .../stage3_tj4d_full_eval_noinfertime_w2_complete/.../official_ckpt_full_eval
  - ****************Evaluation done.*****************
- files changed:
  - local runtime artifact dir (untracked): output/stage3/local_cfgs/hgsfusion_tj4d_stage3_full_eval/stage3_tj4d_full_eval_noinfertime_w2_complete/eval/epoch_4/val/official_ckpt_full_eval/
- reason: execute full Stage 3B TJ4D official-checkpoint evaluation using validated runtime-control path
- next action or blocker: run TJ4D contract checker and metric parser on completed eval dir

### 2026-05-14T15:13:07+08:00
- title: Stage 3B completed eval-dir locate and first validation pass
- current branch: hgsfusion-stage3-full-official-eval
- working directory: /home/user/HGSFusion_research/HGSFusion
- command block executed:
  find output/stage3/local_cfgs/hgsfusion_tj4d_stage3_full_eval -type d -path '*stage3_tj4d_full_eval_noinfertime_w2_complete/eval/*/val/official_ckpt_full_eval' | sort
  source /home/user/miniforge3/etc/profile.d/conda.sh
  conda activate hgsfusion_a17
  EVAL_DIR=output/stage3/local_cfgs/hgsfusion_tj4d_stage3_full_eval/stage3_tj4d_full_eval_noinfertime_w2_complete/eval/epoch_4/val/official_ckpt_full_eval
  python reproduction/stage3/scripts/stage3_eval_contract_check.py --dataset tj4d --info-pkl data/tj4d/kitti_infos_val.pkl --eval-dir "$EVAL_DIR"
  python reproduction/stage3/scripts/stage3_parse_eval_metrics.py --dataset tj4d --eval-dir "$EVAL_DIR" --out-json reproduction/stage3/tj4d_stage3_metrics.json --out-csv reproduction/stage3/stage3_metrics_summary.csv
- exit status:
  - eval-dir locate: 0
  - contract checker: 0 (PASS)
  - metric parser: 1 (KeyError '__overall__' in parse_tj4d)
- important output excerpt:
  - eval dir: output/stage3/local_cfgs/hgsfusion_tj4d_stage3_full_eval/stage3_tj4d_full_eval_noinfertime_w2_complete/eval/epoch_4/val/official_ckpt_full_eval
  - contract: result_pkl_exists=True, result_count=2040, prediction_txt_count=2040, weather markers all True, contract_check=PASS
  - parser traceback points to parse_tj4d overall-metric handling order bug (reproduction script issue)
- files changed:
  - reproduction/stage3/stage3_execution_log.md
- reason: perform required Stage 3B post-run validation; identify parser-side blocker before final Stage 3B pass claim
- next action or blocker: apply minimal parser fix and rerun parser to achieve contract+parser pass gate

### 2026-05-14T15:13:07+08:00
- title: Stage 3B parser fix and validation rerun
- current branch: hgsfusion-stage3-full-official-eval
- working directory: /home/user/HGSFusion_research/HGSFusion
- command block executed:
  edit reproduction/stage3/scripts/stage3_parse_eval_metrics.py (parse_tj4d)
  source /home/user/miniforge3/etc/profile.d/conda.sh
  conda activate hgsfusion_a17
  EVAL_DIR=output/stage3/local_cfgs/hgsfusion_tj4d_stage3_full_eval/stage3_tj4d_full_eval_noinfertime_w2_complete/eval/epoch_4/val/official_ckpt_full_eval
  python reproduction/stage3/scripts/stage3_eval_contract_check.py --dataset tj4d --info-pkl data/tj4d/kitti_infos_val.pkl --eval-dir "$EVAL_DIR"
  python reproduction/stage3/scripts/stage3_parse_eval_metrics.py --dataset tj4d --eval-dir "$EVAL_DIR" --out-json reproduction/stage3/tj4d_stage3_metrics.json --out-csv reproduction/stage3/stage3_metrics_summary.csv
- exit status:
  - contract checker: 0 (PASS)
  - metric parser: 0 (status ok)
- important output excerpt:
  - parser fix: handle `current_class == "__overall__"` metric lines before class-metric assignment
  - parser output: status=ok, parser_notes_count=0
  - outputs written: reproduction/stage3/tj4d_stage3_metrics.json and updated reproduction/stage3/stage3_metrics_summary.csv
- files changed:
  - reproduction/stage3/scripts/stage3_parse_eval_metrics.py
  - reproduction/stage3/tj4d_stage3_metrics.json
  - reproduction/stage3/stage3_metrics_summary.csv
  - reproduction/stage3/stage3_execution_log.md
- reason: clear Stage 3B parser-side blocker and satisfy required contract+parser pass gate before any final hygiene
- next action or blocker: update Stage 3 reproduction notes and commit allowed tracked changes only

### 2026-05-14T15:18:36+08:00
- title: Stage 3 final hygiene verification
- current branch: hgsfusion-stage3-full-official-eval
- working directory: /home/user/HGSFusion_research/HGSFusion
- command block executed:
  git branch --show-current
  git status --short
  git diff --stat
  git diff -- README.md README_UPSTREAM.md reproduction/stage0 reproduction/stage1 reproduction/stage2 || true
  find . \( -path './output' -o -path '*/final_result' -o -name 'result.pkl' -o -name '*.pyc' -o -name '__pycache__' -o -name 'core*' \) -print
  find -L data -name 'kitti_infos_stage3_*.pkl' -print || true
  find -L data -name 'kitti_infos_stage2_*.pkl' -print || true
- exit status: 0
- important output excerpt:
  - current branch confirmed: hgsfusion-stage3-full-official-eval
  - git status --short: empty (clean working tree before final-hygiene note updates)
  - git diff --stat: empty
  - forbidden paths diff (`README.md`, `README_UPSTREAM.md`, `reproduction/stage0`, `reproduction/stage1`, `reproduction/stage2`): empty
  - runtime artifacts discovered locally (untracked by policy): `./output/.../final_result`, `./output/.../result.pkl`, plus many `__pycache__` and `*.pyc`
  - stage3 info pkl pattern: no matches (`kitti_infos_stage3_*.pkl`)
  - stage2 subset info pkls still present: `data/tj4d/kitti_infos_stage2_tj4d_eval_subset20.pkl`, `data/vod_radar_5frames/kitti_infos_stage2_vod_val_subset20.pkl`
- files changed:
  - reproduction/stage3/stage3_execution_log.md
- reason: execute required final hygiene checks after Stage 3A/3B/3C pass and before final Stage 3 closure
- next action or blocker: finalize Stage 3 notes and commit allowed tracked changes only
