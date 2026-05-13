# HGSFusion A′ Reproduction Notes

## Paths

- Repository root: `/home/user/HGSFusion_research/HGSFusion`
- Stable shared data root: `/home/user/HGSFusion_research/data`
- Repository-local compatibility link: `/home/user/HGSFusion_research/HGSFusion/data -> ../data`

Create the repository-local compatibility symlink locally (do not commit it):

```bash
cd /home/user/HGSFusion_research/HGSFusion
ln -s ../data data
```

Use commands from the repository root unless noted.

## Install Command Updates

Legacy command:

```bash
python setup.py develop
```

Replace with:

```bash
python -m pip install -e . --no-build-isolation
```

For pillar ops, use Linux path:

```bash
cd pcdet/ops/pillar_ops
python -m pip install -e . --no-build-isolation
```

## Evaluation Command Typo

Legacy typo:

```bash
--ckpy
```

Correct argument:

```bash
--ckpt
```

## CUDA Compiler Rule

For CUDA extension builds, `nvcc` major version should match `torch.version.cuda`.

For `torch 1.13.1+cu117`:

- use `/usr/local/cuda-11.7/bin/nvcc`
- do not compile extensions with CUDA 12.x `nvcc`

## Hybrid Radar Points Scope

Use official released hybrid radar points first.

Mask2Former-based hybrid point generation is deferred and not part of A′ baseline setup.
