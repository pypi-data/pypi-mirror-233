"""
Print all files from FlutterSDK folder.
"""


import os
import sys

FLUTTER_SDK = "FlutterSDK"
MAX_DEPTH = 4


def print_dir(path: str, max_depth: int) -> None:
    """Walk directory."""
    for root, _, files in os.walk(path):
        depth = root[len(path) + 1 :].count(os.sep)
        if depth >= max_depth:
            continue
        for file in files:
            print(os.path.join(root, file), end="\n")


def main() -> int:
    """Main function."""
    print_dir(FLUTTER_SDK, MAX_DEPTH)
    return 0


if __name__ == "__main__":
    sys.exit(main())
