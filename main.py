#!/usr/bin/env python3
"""make.fun entry for news-image-20261121.

Writes the pre-built news-summary image stored in this repository
(entry.png) to /output/entry.png. Stdlib only, no network, fully
deterministic: every run writes exactly the same bytes.
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
OUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
OUT = os.path.join(OUT_DIR, "entry.png")


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    shutil.copyfile(SRC, OUT)


if __name__ == "__main__":
    main()
