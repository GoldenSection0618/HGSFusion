# HGSFusion Reproduction

This repository is a reproduction-oriented fork of the upstream HGSFusion implementation.

The original upstream README has been preserved as:

```text
README_UPSTREAM.md
```

This root README documents my staged reproduction work, current progress, verified results, and navigation for reproduction artifacts.

## Project Origin

This project is based on the upstream HGSFusion implementation for radar-camera 3D object detection.

The upstream repository provides the original model code, training/evaluation entry points, dataset interfaces, and basic reproduction instructions. In this fork, I keep the upstream implementation as the base and add a traceable reproduction layer around environment setup, compatibility fixes, data-index preparation, and smoke validation.

## What I Have Done

My work so far focuses on making the old upstream codebase reproducible in a controlled local environment.

The main completed work includes:

* Built a reproducible Python 3.9 environment for the legacy HGSFusion codebase.
* Aligned PyTorch CUDA runtime and CUDA extension compiler toolchain.
* Replaced legacy `python setup.py develop` usage with modern editable install commands.
* Compiled and verified HGSFusion/OpenPCDet CUDA extensions.
* Compiled and verified `pillar_cuda`.
* Fixed dataset import leakage so VoD/TJ4D paths do not require unused Argoverse2 dependencies.
* Normalized dataset path handling for the local `data -> ../data` interface.
* Generated and validated VoD/TJ4D `kitti_infos_*.pkl` dataset index files.
* Added a Stage 0 smoke-check script.
* Verified minimal dataloader construction for both VoD and TJ4D.

This is not yet a full training or paper-metric reproduction.

## Current Status

Current stage:

```text
Stage 0 completed: Environment and data-index baseline
```

Verified results:

| Component                             | Status      |
| ------------------------------------- | ----------- |
| Python environment                    | Passed      |
| PyTorch + CUDA runtime                | Passed      |
| CUDA 11.7 compiler alignment          | Passed      |
| MMCV / MMEngine / MMDetection imports | Passed      |
| HGSFusion CUDA extensions             | Passed      |
| `pillar_cuda` import                  | Passed      |
| VoD config load                       | Passed      |
| TJ4D config load                      | Passed      |
| VoD `kitti_infos_*.pkl` generation    | Passed      |
| TJ4D `kitti_infos_*.pkl` generation   | Passed      |
| Stage 0 smoke check                   | Passed      |
| VoD minimal dataloader test           | Passed      |
| TJ4D minimal dataloader test          | Passed      |
| Full training                         | Not started |
| Official checkpoint evaluation        | Not started |
| Paper metric reproduction             | Not started |

## Verified Stage 0 Environment

The Stage 0 baseline uses:

```text
Python: 3.9.23
PyTorch: 1.13.1+cu117
torch.version.cuda: 11.7
Torchvision: 0.14.1+cu117
MMCV: 2.1.0
MMEngine: 0.10.7
MMDetection: 3.3.0
CUDA_HOME: /usr/local/cuda-11.7
nvcc: /usr/local/cuda-11.7/bin/nvcc
```

The CUDA extension build uses CUDA Toolkit 11.7, not the system's newer CUDA compiler.

## Data Interface

The local repository uses a compatibility symlink:

```text
data -> ../data
```

Expected local layout:

```text
/home/user/HGSFusion_research/
├── HGSFusion/
│   └── data -> ../data
└── data/
    ├── vod_radar_5frames/
    └── tj4d/
```

The symlink is local-only and should not be committed.

Create it with:

```bash
cd /home/user/HGSFusion_research/HGSFusion
ln -s ../data data
```

Generated data artifacts such as `kitti_infos_*.pkl`, official hybrid radar points, raw datasets, and checkpoints are not committed to Git.

## Stage 0 Dataset Info Results

Generated and validated dataset info files:

```text
VoD:
train      5139
val        1296
trainval   6435
test       2247

TJ4D:
train      5717
val        2040
trainval   7757
test       2040
```

Note: in the current TJ4D package, `ImageSets/val.txt` is absent. The Stage 0 compatibility fix generates `kitti_infos_val.pkl` using the test split as fallback. This should be considered when interpreting later validation results.

## Quick Validation

Activate the reproduction environment:

```bash
source /home/user/miniforge3/etc/profile.d/conda.sh
conda activate hgsfusion_a17

export CUDA_HOME=/usr/local/cuda-11.7
export PATH=/usr/local/cuda-11.7/bin:$PATH
export LD_LIBRARY_PATH=$CONDA_PREFIX/lib:$CONDA_PREFIX/lib/python3.9/site-packages/torch/lib:/usr/local/cuda-11.7/lib64:${LD_LIBRARY_PATH:-}
```

Run the Stage 0 smoke check from the repository root:

```bash
cd /home/user/HGSFusion_research/HGSFusion
python reproduction/stage0/scripts/hgsfusion_smoke_check.py
```

Expected result:

```text
SMOKE CHECK PASSED
```

## Reproduction Artifacts

Stage 0 reproduction materials are stored under:

```text
reproduction/stage0/
```

Current contents:

```text
reproduction/stage0/
├── scripts/
│   └── hgsfusion_smoke_check.py
├── stage0_execution_log.md
└── stage0_reproduction_notes.md
```

File roles:

* `stage0_execution_log.md`: append-only command/result log for Stage 0.
* `stage0_reproduction_notes.md`: stable setup notes, path rules, and environment decisions.
* `scripts/hgsfusion_smoke_check.py`: Stage 0 smoke-check script.

## Important Notes

The original upstream README has been renamed to:

```text
README_UPSTREAM.md
```

Use it for the original authors' documentation and baseline project instructions.

Use this README for the reproduction status of this fork.

## Current Boundary

Stage 0 verifies that the codebase can be installed, compiled, indexed, and minimally loaded.

Stage 0 does not verify:

* full training,
* official checkpoint loading,
* single-batch model forward,
* full evaluation,
* paper metric reproduction,
* Mask2Former-based hybrid point generation.

## Next Stage

Recommended next stage:

```text
Stage 1: checkpoint/config/model-build validation
```

Suggested Stage 1 tasks:

1. Verify official checkpoint file paths.
2. Build the HGSFusion model from config.
3. Load official checkpoints.
4. Check checkpoint key compatibility.
5. Run a single-batch forward or evaluation dry run.
6. Only then consider full evaluation or training.

## Commit Discipline

The reproduction process is documented through Git commits and the Stage 0 execution log.

Data artifacts are intentionally excluded from Git:

```text
data/
*.pkl
official hybrid points
raw datasets
checkpoints
```
