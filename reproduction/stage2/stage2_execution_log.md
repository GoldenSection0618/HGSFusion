# HGSFusion Stage 2 Execution Log

This file is an append-only command/result log for Stage 2.

Stage 2 scope:
- limited official-checkpoint evaluation dry run
- controlled subset evaluation through `tools/test.py`
- `result.pkl` / `final_result` artifact validation
- evaluation log validation

Out of scope:
- full training
- full benchmark evaluation
- paper metric reproduction
- TTA evaluation
- distributed evaluation
- modifying root `README.md`
- modifying `README_UPSTREAM.md`
- modifying `reproduction/stage0/`
- modifying `reproduction/stage1/`
- committing data artifacts, checkpoints, raw datasets, output files, or data symlinks

## Execution Log

### 2026-05-13T23:31:49+08:00
- current branch:                                     `hgsfusion-stage2-limited-eval-dryrun`
- working directory:                                     `/home/user/HGSFusion_research/HGSFusion`
- command block executed:
  ```bash
  cd /home/user/HGSFusion_research/HGSFusion
  pwd
  git branch --show-current
  git status --short
  git branch --list hgsfusion-stage2-limited-eval-dryrun
  mkdir -p reproduction/stage2/scripts
  create reproduction/stage2/stage2_execution_log.md (template)
  create reproduction/stage2/stage2_reproduction_notes.md (template)
  ```
- exit status: `0`
- important output excerpt:
  - `pwd` = `/home/user/HGSFusion_research/HGSFusion`
  - current branch before init = `hgsfusion-stage2-limited-eval-dryrun`
  - `git status --short` empty (clean worktree before Stage 2 init)
  - Stage 2 branch already existed locally, so switched/kept on existing branch path (no re-create)
  - Stage 1 merged-into-main baseline is assumed by repository governance in AGENT.md; explicit closure evidence will be collected in Section 5 log step
  - initialized Stage 2 directory and template docs
- files changed:
  - `reproduction/stage2/stage2_execution_log.md`
  - `reproduction/stage2/stage2_reproduction_notes.md`
- reason: create Stage 2 branch context and initialize Stage 2 logging before running closure checks
- next action or blocker: run Stage 1 closure check command block and append results

### 2026-05-13T23:32:30+08:00
- current branch:   `hgsfusion-stage2-limited-eval-dryrun`
- working directory:   `/home/user/HGSFusion_research/HGSFusion`
- command block executed:
  ```bash
  cd /home/user/HGSFusion_research/HGSFusion

  pwd
  git branch --show-current
  git status --short
  git log --oneline --decorate -10

  git diff --stat main...HEAD || true
  git diff -- README.md README_UPSTREAM.md reproduction/stage0 reproduction/stage1 || true
  git diff -- pcdet/models/backbones_3d/vfe/fusion_vfe.py || true

  find . \( -path './output' -o -name '*.pyc' -o -name '__pycache__' \) -print

  git merge-base --is-ancestor b05772b main
  git branch --contains b05772b
  ```
- exit status: `0`
- important output excerpt:
  - current branch = `hgsfusion-stage2-limited-eval-dryrun`
  - working tree was clean before closure log append
  - `main...HEAD` diff limited to Stage 2 docs at this moment
  - no diffs in `README.md`, `README_UPSTREAM.md`, `reproduction/stage0`, `reproduction/stage1`
  - no diff in `pcdet/models/backbones_3d/vfe/fusion_vfe.py`
  - local runtime caches/pyc directories exist but were not staged
  - `git merge-base --is-ancestor b05772b main` succeeded (exit 0), confirming Stage 1 anchor commit is contained in `main`
- files changed:
  - `reproduction/stage2/stage2_execution_log.md`
- reason: Stage 1 closure check after Stage 2 log initialization
- next action or blocker: run TJ4D split evidence check and create Stage 2 helper scripts

### 2026-05-13T23:33:09+08:00
- current branch: `hgsfusion-stage2-limited-eval-dryrun`
- working directory: `/home/user/HGSFusion_research/HGSFusion`
- command block executed:
  ```bash
  cd /home/user/HGSFusion_research/HGSFusion

  ls -la data/tj4d/ImageSets || true
  cat data/tj4d/ImageSets/readme.txt || true
  find data/tj4d/ImageSets -maxdepth 1 -type f -print -exec wc -l {} \; || true

  # follow symlink to get file counts from real target
  find -L data/tj4d/ImageSets -maxdepth 1 -type f -print -exec wc -l {} \; || true
  ```
- exit status: `0`
- important output excerpt:
  - `data/tj4d/ImageSets` is a symlink to `/home/user/HGSFusion_research/artifacts/tj4d_sanitized/ImageSets`
  - `readme.txt` states there is no separate validation split and `trainval.txt` equals `all.txt`
  - split line counts (followed symlink): `train.txt=5717`, `test.txt=2040`, `all.txt=7757`, `trainval.txt=7757`
  - interpretation recorded: TJ4D uses official eval split / test-val alias convention, not independent train/val/test
- files changed:
  - `reproduction/stage2/stage2_execution_log.md`
  - `reproduction/stage2/stage2_reproduction_notes.md` (next edit in same batch)
- reason: confirm TJ4D split evidence locally before Stage 2B evaluation
- next action or blocker: implement Stage 2 helper scripts and local Stage 2 config files

### 2026-05-13T23:35:28+08:00
- current branch: `hgsfusion-stage2-limited-eval-dryrun`
- working directory: `/home/user/HGSFusion_research/HGSFusion`
- command block executed:
  ```bash
  cd /home/user/HGSFusion_research/HGSFusion

  # create Stage 2 helper scripts
  create reproduction/stage2/scripts/stage2_make_eval_subset.py
  create reproduction/stage2/scripts/stage2_result_pkl_check.py
  create reproduction/stage2/scripts/stage2_eval_artifact_check.py
  chmod +x reproduction/stage2/scripts/*.py

  # quick cli self-checks
  python reproduction/stage2/scripts/stage2_make_eval_subset.py --help
  python reproduction/stage2/scripts/stage2_result_pkl_check.py --help
  python reproduction/stage2/scripts/stage2_eval_artifact_check.py --help

  # create local cfg copies and adjust only INFO_PATH.test
  mkdir -p reproduction/stage2/local_cfgs
  cp tools/cfgs/hgsfusion/hgsfusion_vod.yaml reproduction/stage2/local_cfgs/hgsfusion_vod_stage2_subset20.yaml
  cp tools/cfgs/hgsfusion/hgsfusion_tj4d.yaml reproduction/stage2/local_cfgs/hgsfusion_tj4d_stage2_subset20.yaml

  # verify local cfg diffs only inject INFO_PATH.test
  diff -u tools/cfgs/hgsfusion/hgsfusion_vod.yaml reproduction/stage2/local_cfgs/hgsfusion_vod_stage2_subset20.yaml
  diff -u tools/cfgs/hgsfusion/hgsfusion_tj4d.yaml reproduction/stage2/local_cfgs/hgsfusion_tj4d_stage2_subset20.yaml
  ```
- exit status: `0`
- important output excerpt:
  - all three helper scripts parse args correctly via `--help`
  - local cfg diffs only add `DATA_CONFIG.INFO_PATH.test` entries for subset pkl files
  - no topology/hyperparameter/NMS/threshold/model-head changes introduced
  - local cfg files are relative-path based and contain no machine-specific absolute paths
- files changed:
  - `reproduction/stage2/scripts/stage2_make_eval_subset.py`
  - `reproduction/stage2/scripts/stage2_result_pkl_check.py`
  - `reproduction/stage2/scripts/stage2_eval_artifact_check.py`
  - `reproduction/stage2/local_cfgs/hgsfusion_vod_stage2_subset20.yaml`
  - `reproduction/stage2/local_cfgs/hgsfusion_tj4d_stage2_subset20.yaml`
  - `reproduction/stage2/stage2_execution_log.md`
- reason: create Stage 2 helper scripts and local subset-only eval configs
- next action or blocker: run Stage 2A VoD subset generation and official-checkpoint evaluation
