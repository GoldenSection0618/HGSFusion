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

## Stage 4C: Single-GPU Bounded Training Smoke

## Stage 4D: Checkpoint Save And Resume

## Stage 4E: Train-After-Eval Artifact Validation

## Stage 4F: DDP + SyncBN Smoke

## Stage 4G: TJ4D Bounded Training Smoke

## Stage 4 Results

Pending.

## Code Fixes Applied Outside reproduction/stage4/

None so far.

## Runtime Artifacts Kept Locally

Pending.

## Files Changed In Stage 4

- `reproduction/stage4/stage4_execution_log.md`
- `reproduction/stage4/stage4_reproduction_notes.md`

## Final Hygiene Result

Pending.

## Next Stage Boundary

Stage 4 validates that the bounded training chain is operational on controlled subsets. It does not claim full training reproduction, full benchmark reproduction, paper-level metric reproduction, or full HGSFusion paper reproduction.
