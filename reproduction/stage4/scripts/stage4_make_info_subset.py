#!/usr/bin/env python3
"""Create bounded info-pkl subsets for Stage 4."""

import argparse
import pickle
import random
from pathlib import Path
from typing import Any, Optional


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", required=True, choices=("vod", "tj4d"))
    parser.add_argument("--source", required=True, help="Source info pkl path")
    parser.add_argument("--output", required=True, help="Output subset pkl path")
    parser.add_argument("--count", required=True, type=int, help="Subset size")
    parser.add_argument("--seed", type=int, default=None, help="Optional random seed")
    return parser.parse_args()


def safe_frame_id(item: Any) -> Optional[str]:
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


def main() -> int:
    args = parse_args()
    if args.count <= 0:
        raise ValueError("--count must be > 0")

    source = Path(args.source)
    output = Path(args.output)
    if not source.exists():
        raise FileNotFoundError(f"source info pkl not found: {source}")

    with source.open("rb") as f:
        data = pickle.load(f)
    if not isinstance(data, list):
        raise TypeError(f"source info pkl must be list, got {type(data).__name__}")
    if args.count > len(data):
        raise ValueError(f"count={args.count} exceeds source length={len(data)}")

    if args.seed is None:
        subset = data[: args.count]
    else:
        rng = random.Random(args.seed)
        selected = set(rng.sample(range(len(data)), args.count))
        subset = [item for i, item in enumerate(data) if i in selected]

    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("wb") as f:
        pickle.dump(subset, f)

    first_frame = safe_frame_id(subset[0]) if subset else None
    last_frame = safe_frame_id(subset[-1]) if subset else None

    print(f"dataset: {args.dataset}")
    print(f"source_path: {source}")
    print(f"output_path: {output}")
    print(f"source_length: {len(data)}")
    print(f"output_length: {len(subset)}")
    print(f"seed: {args.seed}")
    print(f"first_frame_id: {first_frame}")
    print(f"last_frame_id: {last_frame}")
    print("note: generated subset pkl is a runtime artifact and must not be committed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
