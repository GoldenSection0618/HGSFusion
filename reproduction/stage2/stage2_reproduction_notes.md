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

## Stage 2 Results

### Stage 2A: VoD subset evaluation

Status: pending

### Stage 2B: TJ4D subset evaluation

Status: pending

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
