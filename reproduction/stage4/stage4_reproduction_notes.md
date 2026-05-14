# HGSFusion Stage 4 Reproduction Notes

## Scope

Stage 4 validates the bounded training chain is operational on controlled subsets, including:
- `training=True` dataloader construction
- training data contract
- augmentation path
- training forward/backward path
- optimizer step and scheduler step path
- checkpoint save/resume
- train-after-eval artifact generation
- minimal DDP + SyncBN launch (if hardware allows)

## Out of Scope

- full VoD training reproduction
- full TJ4D training reproduction
- full benchmark reproduction
- paper-level metric reproduction
- TTA evaluation
- Mask2Former-based hybrid point generation

## Paths

- Repository root: `/home/user/HGSFusion_research/HGSFusion`
- Stage 4 branch: `hgsfusion-stage4-training-chain-validation`
- Repository data root: `/home/user/HGSFusion_research/HGSFusion/data`
- Checkpoint root: `/home/user/HGSFusion_research/checkpoints`

## Baseline Dependency

- Stage 0, Stage 1, Stage 2, Stage 3 outputs/logs already exist locally.
- Stage 4 assumes Stage 3 full official-checkpoint evaluation has completed.

## README Policy

Do not modify:
- `README.md`
- `README_UPSTREAM.md`
- `reproduction/stage0/`
- `reproduction/stage1/`
- `reproduction/stage2/`
- `reproduction/stage3/`

## Artifact Policy

Runtime artifacts may be generated locally, but must remain untracked and uncommitted:
- data subset `*.pkl`
- `output/`
- checkpoints (`*.pth`, `*.pt`, `*.ckpt`)
- `result.pkl`, prediction txt files, `final_result/`
- logs, `__pycache__`, `*.pyc`

## Stage 4 Plan

1. Stage 4A: preflight and protected-path integrity checks.
2. Stage 4B: training data contract checks for VoD/TJ4D with `training=True`.
3. Stage 4C: bounded VoD single-GPU training smoke + parser.
4. Stage 4D: checkpoint resume validation.
5. Stage 4E: train-after-eval artifact validation.
6. Stage 4F: DDP + SyncBN smoke or hardware-based skip.
7. Stage 4G: bounded TJ4D single-GPU training smoke.
8. Runtime summary + final hygiene checks.

## Stage 4A: Preflight And Repository State

- current branch: `hgsfusion-stage4-training-chain-validation`
- working directory: `/home/user/HGSFusion_research/HGSFusion`
- protected paths diff: clean (`README.md`, `README_UPSTREAM.md`, `reproduction/stage0-3`)
- Stage 3 exists locally: yes (`reproduction/stage3/` present)
- Stage 4 docs initialized: yes

## Stage 4B: Training Data Contract

- VoD: passed
  - command:
    - `python reproduction/stage4/scripts/stage4_train_data_contract_check.py --dataset vod --batch-size 1 --workers 0 --max-batches 2`
  - dataset length: `5139`
  - required keys all present in checked batches:
    - `points`, `images`, `gt_boxes`, `gt_boxes2d`, `image_shape`, `trans_lidar_to_cam`, `trans_cam_to_img`, `lidar_aug_matrix`, `frame_id`, `batch_size`
  - summary marker:
    - `TRAIN_DATA_CONTRACT_OK dataset=vod batches_checked=2`

- TJ4D: passed
  - command:
    - `python reproduction/stage4/scripts/stage4_train_data_contract_check.py --dataset tj4d --batch-size 1 --workers 0 --max-batches 2`
  - dataset length: `5717`
  - required keys all present in checked batches
  - summary marker:
    - `TRAIN_DATA_CONTRACT_OK dataset=tj4d batches_checked=2`

- warnings:
  - Numba deprecation warnings observed during import/eval helper load; no blocking runtime failure.

- interpretation:
  - this stage validates training-side batch contract only, not end-to-end training success.

## Stage 4C: Single-GPU Bounded Training Smoke

- subset files generated (runtime-only, untracked):
  - `data/vod_radar_5frames/kitti_infos_stage4_vod_train20.pkl` (20)
  - `data/vod_radar_5frames/kitti_infos_stage4_vod_train80.pkl` (80)
  - `data/vod_radar_5frames/kitti_infos_stage4_vod_eval20.pkl` (20)
  - `data/tj4d/kitti_infos_stage4_tj4d_train20.pkl` (20)
  - `data/tj4d/kitti_infos_stage4_tj4d_eval20.pkl` (20)

- VoD single-GPU bounded train command:
  - `CUDA_VISIBLE_DEVICES=0 python tools/train.py --cfg_file reproduction/stage4/local_cfgs/hgsfusion_vod_stage4_train20.yaml --batch_size 1 --workers 2 --epochs 1 --extra_tag stage4_vod_train20_e1_sg --fix_random_seed --ckpt_save_interval 1 --max_ckpt_save_num 2`
- output directory:
  - `output/stage4/local_cfgs/hgsfusion_vod_stage4_train20/stage4_vod_train20_e1_sg`
- checkpoint directory:
  - `output/stage4/local_cfgs/hgsfusion_vod_stage4_train20/stage4_vod_train20_e1_sg/ckpt`
- train log:
  - `output/stage4/local_cfgs/hgsfusion_vod_stage4_train20/stage4_vod_train20_e1_sg/train_20260514-162309.log`
- status:
  - training completed
  - finite loss observed (`3.569 -> 2.860`, no NaN/Inf)
  - checkpoint saved (`checkpoint_epoch_1.pth`)
  - train-after-eval executed
  - bounded eval subset confirmed via local cfg (`kitti_infos_stage4_vod_eval20.pkl`)

## Stage 4D: Checkpoint Save And Resume

- source checkpoint:
  - `output/stage4/local_cfgs/hgsfusion_vod_stage4_train20/stage4_vod_train20_e1_sg/ckpt/checkpoint_epoch_1.pth`
- resume command:
  - `CUDA_VISIBLE_DEVICES=0 python tools/train.py --cfg_file reproduction/stage4/local_cfgs/hgsfusion_vod_stage4_train20.yaml --batch_size 1 --workers 2 --epochs 2 --ckpt output/stage4/local_cfgs/hgsfusion_vod_stage4_train20/stage4_vod_train20_e1_sg/ckpt/checkpoint_epoch_1.pth --extra_tag stage4_vod_train20_resume_e2_sg --fix_random_seed --ckpt_save_interval 1 --max_ckpt_save_num 2`
- resume behavior:
  - checkpoint load succeeded
  - optimizer state load path succeeded (`load_params_with_optimizer`)
  - resumed at epoch 2 loop (no incorrect restart from epoch 0)
  - additional epoch executed
- resulting checkpoint:
  - `output/stage4/local_cfgs/hgsfusion_vod_stage4_train20/stage4_vod_train20_resume_e2_sg/ckpt/checkpoint_epoch_2.pth`
- loss finiteness:
  - finite (`2.112`, `2.124`; no NaN/Inf)
- interpretation:
  - pass

## Stage 4E: Train-After-Eval Artifact Validation

- VoD epoch-1 eval artifacts:
  - eval dir:
    - `output/stage4/local_cfgs/hgsfusion_vod_stage4_train20/stage4_vod_train20_e1_sg/eval/eval_with_train/epoch_1/val`
  - checker command:
    - `python reproduction/stage4/scripts/stage4_train_artifact_check.py --eval-output-dir .../epoch_1/val --expected-count 20`
  - result:
    - `TRAIN_AFTER_EVAL_ARTIFACT_CHECK_OK expected=20 actual=20`

- VoD resume epoch-2 eval artifacts:
  - eval dir:
    - `output/stage4/local_cfgs/hgsfusion_vod_stage4_train20/stage4_vod_train20_resume_e2_sg/eval/eval_with_train/epoch_2/val`
  - checker result: pass (`expected=20`, `actual=20`)

- checker robustness fix:
  - `stage4_train_artifact_check.py` adjusted to fallback to `train_*.log` when standalone `log_eval_*.txt` is absent in train-after-eval workflow.

- interpretation:
  - validates artifact generation path (`result.pkl`, prediction txt files, completion log markers), not metric quality.

## Stage 4F: DDP + SyncBN Smoke

- GPU count probe:
  - `cuda_available: True`
  - `device_count: 1`
  - `0 NVIDIA GeForce RTX 4060 Laptop GPU`
- status:
  - DDP + SyncBN smoke skipped due hardware limitation (`<2 GPUs`)
- limitation:
  - distributed launch and SyncBN conversion were not validated in this environment.

## Stage 4G: TJ4D Bounded Training Smoke

- TJ4D split interpretation:
  - `TJ4D kitti_infos_val.pkl is interpreted as the official eval split / test-val alias split, not as an independent validation split.`

- initial command (required shape):
  - `CUDA_VISIBLE_DEVICES=0 python tools/train.py --cfg_file reproduction/stage4/local_cfgs/hgsfusion_tj4d_stage4_train20.yaml --batch_size 1 --workers 2 --epochs 1 --extra_tag stage4_tj4d_train20_e1_sg --fix_random_seed --ckpt_save_interval 1 --max_ckpt_save_num 2`
- initial result:
  - training completed
  - evaluation produced metrics and artifacts
  - process failed at TensorBoard write in `repeat_eval_ckpt`:
    - `NotImplementedError: Got <class 'dict'>, but expected numpy array or torch tensor.`

- minimal blocker fix outside `reproduction/stage4/`:
  - file:
    - `tools/test.py`
  - fix:
    - in `repeat_eval_ckpt`, write to TensorBoard only for scalar metric values; skip non-scalar dict metrics with warning.

- rerun command after fix:
  - `CUDA_VISIBLE_DEVICES=0 python tools/train.py --cfg_file reproduction/stage4/local_cfgs/hgsfusion_tj4d_stage4_train20.yaml --batch_size 1 --workers 2 --epochs 1 --extra_tag stage4_tj4d_train20_e1_sg_fix1 --fix_random_seed --ckpt_save_interval 1 --max_ckpt_save_num 2`
- rerun result:
  - training completed
  - train-after-eval completed
  - weather markers present (`Evaluating dark/standard/shiny/all_weather`)
  - completion marker present (`End evaluation ...`)
  - checkpoint created:
    - `output/stage4/local_cfgs/hgsfusion_tj4d_stage4_train20/stage4_tj4d_train20_e1_sg_fix1/ckpt/checkpoint_epoch_1.pth`

## Stage 4 Results

Stage 4 completed with one documented blocker fix.

Validated items:
- `training=True` dataloader construction
- training batch contract for VoD/TJ4D
- augmentation path in bounded train loops
- forward/backward/optimizer step
- finite training loss under bounded smoke
- checkpoint save
- checkpoint resume with optimizer state
- train-after-eval artifact generation
- TJ4D train-after-eval weather evaluation path (after minimal blocker fix)
- DDP check gate (hardware-based skip recorded)

Required safe interpretation:
- Stage 4 validates that the bounded training chain is operational on controlled subsets. It does not claim full training reproduction, full benchmark reproduction, paper-level metric reproduction, or full HGSFusion paper reproduction.

## Code Fixes Applied Outside reproduction/stage4/

- `tools/test.py`
  - reason: train-after-eval path for TJ4D emitted nested weather dict metrics and crashed at `tb_log.add_scalar`.
  - minimal fix: skip non-scalar metrics when writing TensorBoard scalars.
  - scope boundary: no model/data/topology/hyperparameter changes.

## Runtime Artifacts Kept Locally

- subset info pkl files:
  - `data/vod_radar_5frames/kitti_infos_stage4_vod_train20.pkl`
  - `data/vod_radar_5frames/kitti_infos_stage4_vod_train80.pkl`
  - `data/vod_radar_5frames/kitti_infos_stage4_vod_eval20.pkl`
  - `data/tj4d/kitti_infos_stage4_tj4d_train20.pkl`
  - `data/tj4d/kitti_infos_stage4_tj4d_eval20.pkl`
- bounded output directories:
  - `output/stage4/local_cfgs/hgsfusion_vod_stage4_train20/stage4_vod_train20_e1_sg/`
  - `output/stage4/local_cfgs/hgsfusion_vod_stage4_train20/stage4_vod_train20_resume_e2_sg/`
  - `output/stage4/local_cfgs/hgsfusion_tj4d_stage4_train20/stage4_tj4d_train20_e1_sg/` (failed run artifact kept for diagnosis)
  - `output/stage4/local_cfgs/hgsfusion_tj4d_stage4_train20/stage4_tj4d_train20_e1_sg_fix1/`

## Files Changed In Stage 4

- `reproduction/stage4/stage4_execution_log.md`
- `reproduction/stage4/stage4_reproduction_notes.md`
- `reproduction/stage4/scripts/stage4_train_data_contract_check.py`
- `reproduction/stage4/scripts/stage4_make_info_subset.py`
- `reproduction/stage4/scripts/stage4_train_log_parser.py`
- `reproduction/stage4/scripts/stage4_train_artifact_check.py`
- `reproduction/stage4/scripts/stage4_runtime_summary.py`
- `reproduction/stage4/local_cfgs/hgsfusion_vod_stage4_train20.yaml`
- `reproduction/stage4/local_cfgs/hgsfusion_tj4d_stage4_train20.yaml`
- `reproduction/stage4/local_cfgs/hgsfusion_vod_stage4_train80_ddp.yaml`
- `reproduction/stage4/outputs/stage4_training_summary.json`
- `reproduction/stage4/outputs/stage4_training_summary.csv`
- `tools/test.py` (minimal blocker fix)

## Final Hygiene Result

- `README.md` unchanged.
- `README_UPSTREAM.md` unchanged.
- `reproduction/stage0/`, `reproduction/stage1/`, `reproduction/stage2/`, `reproduction/stage3/` unchanged.
- runtime artifacts remain untracked and uncommitted.
- Stage 4 modifications are scoped to `reproduction/stage4/` plus one minimal blocker fix in `tools/test.py`.

## Next Stage Boundary

Stage 4 validates that the bounded training chain is operational on controlled subsets. It does not claim full training reproduction, full benchmark reproduction, paper-level metric reproduction, or full HGSFusion paper reproduction.

Recommended boundary:
- Stage 5 should attempt full VoD training reproduction only after Stage 4 pass.
- TJ4D full training should follow only after VoD full training is stable and runtime/storage costs are understood.
