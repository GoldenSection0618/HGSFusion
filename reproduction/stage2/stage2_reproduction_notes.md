# HGSFusion Stage 2 Reproduction Notes

## Scope

Stage 2 validates the repository evaluation path after Stage 1.

Stage 2 focuses on:

- controlled subset evaluation through `tools/test.py`
- official checkpoint evaluation dry run
- prediction artifact generation
- `result.pkl` schema validation
- `final_result/data` validation
- evaluation log validation

Stage 2 does not cover:

- full training
- full benchmark evaluation
- paper metric reproduction
- distributed evaluation
- TTA evaluation
- Mask2Former-based hybrid point generation

## Paths

- Repository root: `/home/user/HGSFusion_research/HGSFusion`
- Data directory used by repository: `/home/user/HGSFusion_research/HGSFusion/data`
- Checkpoint root: `/home/user/HGSFusion_research/checkpoints`
- Official checkpoint files are `.pth` files under `/home/user/HGSFusion_research/checkpoints`
- Output root: `output/`

## Stage 0 And Stage 1 Baseline Dependency

Stage 2 assumes:

- Stage 0 smoke check passed
- VoD/TJ4D `kitti_infos_*.pkl` generated
- CUDA extensions importable
- `pillar_cuda` importable
- Stage 1 model-runtime dry run passed
- official checkpoints load with `936/936`
- single-batch forward passed for VoD and TJ4D

## README Policy

Do not modify:

- `README.md`
- `README_UPSTREAM.md`
- `reproduction/stage0/`
- `reproduction/stage1/`

All Stage 2 notes and command logs must stay under:

```text
reproduction/stage2/
```

## TJ4D Split Note

TJ4DRadSet does not provide an independent three-way `train/val/test` split in the usual machine-learning sense.

The official dataset convention is closer to:

- `train`: training split
- `test(val)`: official labeled evaluation split

In this repository, `kitti_infos_val.pkl` should be interpreted as the TJ4D official eval split / test-val alias split, not as an independent validation split.

This does not block Stage 2 official-checkpoint evaluation dry run. However, any reported metric must clearly state that it is evaluated on the TJ4D official eval split / test-val alias split.

Local evidence (2026-05-13):
- `data/tj4d/ImageSets` -> `/home/user/HGSFusion_research/artifacts/tj4d_sanitized/ImageSets` (symlink)
- `readme.txt` states no separate validation split and says `trainval.txt` equals `all.txt`
- line counts: `train.txt=5717`, `test.txt=2040`, `all.txt=7757`, `trainval.txt=7757`

## Artifact Policy

Stage 2 may temporarily generate subset pkl files and evaluation outputs. These are runtime artifacts only.

Do not commit:

- `data`
- `*.pkl`
- raw datasets
- official hybrid points
- official checkpoints
- generated prediction outputs
- `output/`
- `final_result/`
- `result.pkl`
- prediction txt files from dry runs
- `*.pyc`
- `__pycache__/`
- temporary logs under `/tmp`

If runtime artifacts are kept locally, record their exact paths in this notes file. If they are cleaned up, record the cleanup command and result in `stage2_execution_log.md`.

Local runtime artifacts currently kept (untracked):
- `data/vod_radar_5frames/kitti_infos_stage2_vod_val_subset20.pkl`
- `data/tj4d/kitti_infos_stage2_tj4d_eval_subset20.pkl`
- `output/stage2/local_cfgs/hgsfusion_vod_stage2_subset20/stage2_vod_subset20/eval/epoch_no_number/val/official_ckpt_subset20/`
- `output/stage2/local_cfgs/hgsfusion_tj4d_stage2_subset20/stage2_tj4d_subset20/eval/epoch_4/val/official_ckpt_subset20/`

## Stage 2 Results

## Bug Root Cause And Fix

Root cause of the evaluation-finalization crash (`exit 139`):
- `dataset.evaluation` hit a segfault in numba CUDA JIT initialization while importing `pcdet/datasets/kitti/kitti_object_eval_python/rotate_iou.py`.
- Faulthandler stacks point to `numba.cuda...compile_device` from `rotate_iou.py` import path.
- In VoD and TJ4D dataset wrappers, an unnecessary import of `kitti_object_eval_python.eval` was executed before actual result reporting.
- In TJ4D default eval (`bbox/bev/3d`), BEV/3D IoU path also imported GPU rotate IoU and triggered the same failure on this environment.
- After removing that segfault trigger, an additional Stage 2 subset-only issue surfaced: weather-split evaluation attempted to evaluate an empty subset and raised `ZeroDivisionError`.

Applied minimal fix:
- Removed unused `kitti_object_eval_python.eval` import from:
  - `pcdet/datasets/kitti/vod_dataset.py` (`evaluation`)
  - `pcdet/datasets/kitti/tj4d_dataset.py` (`evaluation`)
- Switched TJ4D BEV/3D IoU overlap helper from GPU numba rotate IoU to existing CPU `rotate_iou_eval`:
  - `pcdet/datasets/kitti/tj4d_utils.py`
- Added empty-weather-subset guard in `pcdet/datasets/kitti/tj4d_dataset.py` to skip subsets with zero matched samples instead of dividing by zero.

Post-fix targeted replay evidence:
- VoD `dataset.evaluation` replay on existing `result.pkl`: returns successfully (no segfault).
- TJ4D `dataset.evaluation` replay on existing `result.pkl`: returns successfully (no segfault, no zero-division).

### Stage 2A: VoD subset evaluation

Status: failed at `dataset.evaluation` stage (process exit 139)

- command used:
  - `python tools/test.py --cfg_file reproduction/stage2/local_cfgs/hgsfusion_vod_stage2_subset20.yaml --ckpt /home/user/HGSFusion_research/checkpoints/hgsfusion_vod.pth --batch_size 1 --workers 0 --extra_tag stage2_vod_subset20 --eval_tag official_ckpt_subset20`
- subset source pkl: `data/vod_radar_5frames/kitti_infos_val.pkl`
- subset output pkl: `data/vod_radar_5frames/kitti_infos_stage2_vod_val_subset20.pkl`
- subset size: `20`
- checkpoint path: `/home/user/HGSFusion_research/checkpoints/hgsfusion_vod.pth`
- eval output dir: `output/stage2/local_cfgs/hgsfusion_vod_stage2_subset20/stage2_vod_subset20/eval/epoch_no_number/val/official_ckpt_subset20`
- result.pkl path: `output/stage2/local_cfgs/hgsfusion_vod_stage2_subset20/stage2_vod_subset20/eval/epoch_no_number/val/official_ckpt_subset20/result.pkl`
- final_result/data status: exists with `20` prediction txt files
- log status:
  - `recall_roi`, `recall_rcnn`, `Average predicted number` present
  - `Result is saved`, `Evaluation done` missing
- pass/fail status:
  - `tools/test.py` exited `139` (segmentation fault)
  - stage pass criteria not met
- interpretation note:
  - this is a controlled subset dry run and not paper metric reproduction

### Stage 2B: TJ4D subset evaluation

Status: failed at `dataset.evaluation` stage (process exit 139)

- command used:
  - `python tools/test.py --cfg_file reproduction/stage2/local_cfgs/hgsfusion_tj4d_stage2_subset20.yaml --ckpt /home/user/HGSFusion_research/checkpoints/hgsfusion_tj4d.pth --batch_size 1 --workers 0 --extra_tag stage2_tj4d_subset20 --eval_tag official_ckpt_subset20`
- subset source pkl: `data/tj4d/kitti_infos_val.pkl`
- subset output pkl: `data/tj4d/kitti_infos_stage2_tj4d_eval_subset20.pkl`
- subset size: `20`
- checkpoint path: `/home/user/HGSFusion_research/checkpoints/hgsfusion_tj4d.pth`
- eval output dir: `output/stage2/local_cfgs/hgsfusion_tj4d_stage2_subset20/stage2_tj4d_subset20/eval/epoch_4/val/official_ckpt_subset20`
- result.pkl path: `output/stage2/local_cfgs/hgsfusion_tj4d_stage2_subset20/stage2_tj4d_subset20/eval/epoch_4/val/official_ckpt_subset20/result.pkl`
- final_result/data status: exists with `20` prediction txt files
- log status:
  - `recall_roi`, `recall_rcnn`, `Average predicted number` present
  - `Result is saved`, `Evaluation done` missing
- pass/fail status:
  - `tools/test.py` exited `139` (segmentation fault)
  - stage pass criteria not met
- split interpretation note:
  - TJ4D metric context is official eval split / test-val alias split
  - this is not an independent validation-set metric claim
- interpretation note:
  - this is a controlled subset dry run and not paper metric reproduction

## Files Changed In Stage 2

Expected committed files:

- `reproduction/stage2/stage2_execution_log.md`
- `reproduction/stage2/stage2_reproduction_notes.md`
- `reproduction/stage2/scripts/stage2_make_eval_subset.py`
- `reproduction/stage2/scripts/stage2_result_pkl_check.py`
- `reproduction/stage2/scripts/stage2_eval_artifact_check.py`

No committed changes should exist in:

- `README.md`
- `README_UPSTREAM.md`
- `reproduction/stage0/`
- `reproduction/stage1/`
- `data/`
- `output/`
- `final_result/`
- generated subset pkl files
- generated dry-run result files
