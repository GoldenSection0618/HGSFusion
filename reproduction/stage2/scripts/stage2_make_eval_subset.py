#!/usr/bin/env python3
"""Create deterministic eval subset pickle files for Stage 2 dry runs."""

import argparse
import os
import pickle
import random
import sys
from typing import Any, Iterable, Optional


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, help="Source info pkl path")
    parser.add_argument("--output", required=True, help="Output subset pkl path")
    parser.add_argument("--count", required=True, type=int, help="Subset size")
    parser.add_argument(
        "--mode",
        required=True,
        choices=["first", "seeded"],
        help="Subset selection mode",
    )
    parser.add_argument("--seed", type=int, default=20260513, help="Seed for seeded mode")
    return parser.parse_args()


def _safe_frame_id(item: Any) -> Optional[str]:
    if not isinstance(item, dict):
        return None
    if "frame_id" in item:
        return str(item["frame_id"])
    point_cloud = item.get("point_cloud")
    if isinstance(point_cloud, dict):
        for key in ("lidar_idx", "frame_id"):
            if key in point_cloud:
                return str(point_cloud[key])
    image = item.get("image")
    if isinstance(image, dict) and "image_idx" in image:
        return str(image["image_idx"])
    return None


def _subset_indices(total: int, count: int, mode: str, seed: int) -> Iterable[int]:
    if mode == "first":
        return range(count)
    rng = random.Random(seed)
    # Sort sampled indices for stable data order in output file.
    return sorted(rng.sample(range(total), count))


def main() -> int:
    args = parse_args()

    if args.count <= 0:
        print("ERROR: --count must be positive", file=sys.stderr)
        return 2

    with open(args.input, "rb") as f:
        source = pickle.load(f)

    if not isinstance(source, list):
        print(f"ERROR: expected source pickle to be list, got {type(source).__name__}", file=sys.stderr)
        return 2

    total = len(source)
    if args.count > total:
        print(f"ERROR: requested count={args.count} exceeds source length={total}", file=sys.stderr)
        return 2

    indices = list(_subset_indices(total, args.count, args.mode, args.seed))
    subset = [source[i] for i in indices]

    os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
    with open(args.output, "wb") as f:
        pickle.dump(subset, f)

    first_frame = _safe_frame_id(subset[0]) if subset else None
    last_frame = _safe_frame_id(subset[-1]) if subset else None

    print(f"source_path: {args.input}")
    print(f"output_path: {args.output}")
    print(f"mode: {args.mode}")
    if args.mode == "seeded":
        print(f"seed: {args.seed}")
    print(f"original_length: {total}")
    print(f"subset_length: {len(subset)}")
    print(f"first_frame_id: {first_frame}")
    print(f"last_frame_id: {last_frame}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
