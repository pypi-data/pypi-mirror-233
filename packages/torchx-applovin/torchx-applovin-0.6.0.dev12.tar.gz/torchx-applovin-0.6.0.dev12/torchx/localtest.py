#!/usr/bin/env python3
import argparse
import os
import sys
import tarfile
import tempfile
import zipfile
from typing import List
from torchx.specs import get_named_resources

def parse_args(argv: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="example data preprocessing",
    )
    parser.add_argument(
        "--input_path",
        type=str,
        help="dataset to download",
        default="http://cs231n.stanford.edu/tiny-imagenet-200.zip",
    )
    parser.add_argument(
        "--output_path",
        type=str,
        help="remote path to save the .tar.gz data to",
        required=True,
    )
    parser.add_argument(
        "--limit",
        type=int,
        help="limit number of processed examples",
    )
    return parser.parse_args(argv)

def main(argv: List[str]) -> None:
    print(get_named_resources("testGPU"))

main(["hi"])
