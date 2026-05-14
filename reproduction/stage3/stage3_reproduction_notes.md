# HGSFusion Stage 3 Reproduction Notes

## Scope
- Stage 3 scope is limited to full official-checkpoint evaluation for VoD and TJ4D through `tools/test.py`.
- Stage 3 validates full artifact contract completion and parses metrics into structured JSON/CSV.
- Stage 3 does not claim full training reproduction or paper-level benchmark reproduction.

## Paths
- Repository root: `/home/user/HGSFusion_research/HGSFusion`
- Data root used by repository: `/home/user/HGSFusion_research/HGSFusion/data`
- Checkpoint root: `/home/user/HGSFusion_research/checkpoints`
- Stage 3 working records root: `reproduction/stage3/`

## Stage 0 / Stage 1 / Stage 2 Baseline Dependency
- Stage 0, Stage 1, and Stage 2 notes/logs were re-read before Stage 3 substantive operations.
- Stage 3 reuses the prior environment contract (`conda activate hgsfusion_a17`, CUDA 11.7, WSL `LD_LIBRARY_PATH` rule).
- Stage 3 assumes Stage 2 evaluation-finalization crash fix boundary already merged on `main`.

## README Policy
- `README.md` is frozen and must remain untouched throughout Stage 3.
- `README_UPSTREAM.md` is frozen and must remain untouched throughout Stage 3.

## TJ4D Split Note
- Stage 3 interprets `data/tj4d/kitti_infos_val.pkl` as the TJ4D official eval split / test-val alias split.
- Stage 3 does not describe TJ4D metrics as an independent conventional validation-split claim.

## Artifact Policy
- Runtime artifacts (`output/`, `result.pkl`, `final_result/data`, prediction txt files, raw data/checkpoint artifacts) are local-only and untracked.
- Stage 3 commits include only allowed reproduction records and scripts/configs under `reproduction/stage3/`, unless a documented minimal source-code blocker fix becomes necessary.

## Stage 3 Results

### Stage 3A: VoD full official-checkpoint evaluation
- status: pending
- info pkl audit baseline: `data/vod_radar_5frames/kitti_infos_val.pkl` -> `type=list`, `len=1296`

### Stage 3B: TJ4D full official-checkpoint evaluation
- status: pending
- info pkl audit baseline: `data/tj4d/kitti_infos_val.pkl` -> `type=list`, `len=2040`
- split interpretation: official eval split / test-val alias split

### Stage 3C: Metric parsing and summary
- status: pending
- target outputs:
  - `reproduction/stage3/vod_stage3_metrics.json`
  - `reproduction/stage3/tj4d_stage3_metrics.json`
  - `reproduction/stage3/stage3_metrics_summary.csv`

## Files Changed In Stage 3
- `reproduction/stage3/stage3_execution_log.md`
- `reproduction/stage3/stage3_reproduction_notes.md`
- `reproduction/stage3/local_cfgs/hgsfusion_vod_stage3_full_eval.yaml`
- `reproduction/stage3/local_cfgs/hgsfusion_tj4d_stage3_full_eval.yaml`
- `reproduction/stage3/scripts/stage3_eval_contract_check.py`
- `reproduction/stage3/scripts/stage3_parse_eval_metrics.py`

## Final Hygiene Result
- pending
