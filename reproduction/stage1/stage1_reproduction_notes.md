# HGSFusion Stage 1 Reproduction Notes

## Scope

Stage 1 validates the model-side runtime chain after Stage 0.

Stage 1 focuses on:

- config path and artifact audit
- dataset-to-model batch contract
- model build
- official checkpoint audit
- official checkpoint load
- single-batch forward
- optional 1-2 batch eval dry run

Stage 1 does not cover:

- full training
- full benchmark evaluation
- paper metric reproduction
- Mask2Former-based hybrid point generation

## Paths

- Codex working directory: `/home/user/HGSFusion_research`
- Repository root: `/home/user/HGSFusion_research/HGSFusion`
- Data directory used by the repository: `/home/user/HGSFusion_research/HGSFusion/data`
- Checkpoint root: `/home/user/HGSFusion_research/checkpoints`
- DeepLabV3 pretrained file: `/home/user/HGSFusion_research/checkpoints/deeplabv3_resnet101_coco-586e9e4e.pth`

## Stage 0 Baseline Dependency

Stage 1 assumes Stage 0 is complete:

- environment reproducible
- CUDA extensions importable
- `pillar_cuda` importable
- VoD/TJ4D `kitti_infos_*.pkl` generated
- Stage 0 smoke check passed
- minimal VoD/TJ4D dataloader checks passed

## README Policy

Do not modify:

- `README.md`, absolutely no modification during Stage 1
- `README_UPSTREAM.md`
- `reproduction/stage0/`

All Stage 1 notes and command logs must stay under:

```text
reproduction/stage1/
```

## TJ4D Split Note

Current TJ4D `kitti_infos_val.pkl` uses the test split as fallback because `ImageSets/val.txt` is absent in the current dataset package.

Do not describe this as a standard TJ4D validation split.

## Artifact Policy

Do not commit:

- `data`
- `*.pkl`
- raw datasets
- official hybrid points
- official checkpoints
- generated prediction outputs
- `output/`
- `*.pyc`
- `__pycache__/`
- temporary logs under `/tmp`

## Checkpoint And Pretrained Path Decisions

- DeepLabV3 pretrained path (required): `/home/user/HGSFusion_research/checkpoints/deeplabv3_resnet101_coco-586e9e4e.pth`
- Official VoD checkpoint path used by Stage 1:
  - link path: `/home/user/HGSFusion_research/checkpoints/hgsfusion_vod.pth`
  - resolved target: `/mnt/e/HGSFusion_datasets/raw/hgsfusion_official_assets/hgsfusion_vod.pth`
- Official TJ4D checkpoint candidate path discovered in checkpoints root:
  - link path: `/home/user/HGSFusion_research/checkpoints/hgsfusion_tj4d.pth`
  - resolved target: `/mnt/e/HGSFusion_datasets/raw/hgsfusion_official_assets/hgsfusion_tj4d.pth`

## Stage 1 Results

### Stage 1A (VoD) Status

- path/artifact audit: passed
- batch contract check: passed
- model build-only: passed
- official checkpoint structural audit: passed
- official checkpoint load (repository path): passed
- single-batch forward dry run: passed
- optional 2-batch eval dry run: passed (limited loop, no metric claim)

VoD key outcomes:

- `len(model.state_dict()) = 936`
- `len(checkpoint['model_state']) = 936`
- matched keys: `936`
- missing keys: `0`
- unexpected keys: `0`
- shape mismatch keys: `0`
- checkpoint loader summary: `Done (loaded 936/936)`
- single-batch forward output schema verified:
  - `pred_boxes` shape `(3, 7)`
  - `pred_scores` shape `(3,)`
  - `pred_labels` shape `(3,)`

### Minimal Compatibility Fixes Applied Outside `reproduction/stage1/`

The following changes were required to unblock Stage 1 model build/runtime and were intentionally kept minimal:

- environment dependency fix:
  - installed `spconv-cu117` in `hgsfusion_a17` to satisfy model import/runtime dependency.
- code compatibility fixes:
  - file changed: `pcdet/models/backbones_3d/vfe/fusion_vfe.py`
  - fix 1: remove import dependency on missing module `feature_sampler`; keep backward-compatible alias `GaussianSampler -> SimpleSampler`.
  - fix 2: make `RadarOccupancy2D` optional import (current VoD/TJ4D configs use `RadarOccupancy2DV2`).
  - fix 3: make `ForegroundSampler` optional import; only raise if config explicitly enables it.

These fixes do not alter model topology for current configs and do not disable core modules used by current Stage 1 paths.

### Runtime Library Note

- For GPU forward on this WSL host, `LD_LIBRARY_PATH` needed `/usr/lib/wsl/lib` so `libcuda.so` is visible to cuDNN runtime.

### Stage 1B (TJ4D) Status

- path/artifact audit: passed
- batch contract check: passed
- model build-only: passed
- official checkpoint structural audit: passed
- official checkpoint load (repository path): passed
- single-batch forward dry run: passed
- optional 2-batch eval dry run: passed (limited loop, no metric claim)

TJ4D key outcomes:

- `len(model.state_dict()) = 936`
- `len(checkpoint['model_state']) = 936`
- matched keys: `936`
- missing keys: `0`
- unexpected keys: `0`
- shape mismatch keys: `0`
- checkpoint loader summary: `Done (loaded 936/936)`
- single-batch forward output schema verified:
  - `pred_boxes` shape `(3, 7)`
  - `pred_scores` shape `(3,)`
  - `pred_labels` shape `(3,)`

TJ4D split interpretation remains unchanged:

- current `kitti_infos_val.pkl` is generated from the test split fallback because `ImageSets/val.txt` is absent in the current dataset package.
- this is not a standard TJ4D validation split.

### Stage 1 Completion Status

Stage 1 completed: checkpoint/config/model-runtime dry run passed for VoD and TJ4D.

### Next Stage Boundary

Recommended next stage:

- Stage 2: limited official-checkpoint evaluation dry run

Still out of scope after Stage 1:

- full training
- full benchmark evaluation
- paper metric reproduction
