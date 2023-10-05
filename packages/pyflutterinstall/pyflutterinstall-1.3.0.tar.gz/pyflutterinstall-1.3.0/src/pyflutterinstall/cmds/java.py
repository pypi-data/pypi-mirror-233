"""
Command stub for sdkmanager
"""

import os
import sys
import warnings

from pyflutterinstall.config import config_load
from pyflutterinstall.trampoline import trampoline

JAVA_DIR = config_load().get("JAVA_DIR", None)

COMMAND = "java"


def find_java_exe(java_base_dir: str) -> str | None:
    """Find bin folder"""
    # use os walk
    for root, dirs, _ in os.walk(java_base_dir):
        if "bin" in dirs:
            bin_dir = os.path.join(root, "bin")
            java_exe = os.path.join(bin_dir, "java")
            if sys.platform == "win32":
                java_exe += ".exe"
            if os.path.isfile(java_exe):
                return java_exe
    return None


def find_default_path_or_none() -> str | None:
    """Find default path"""
    java_dir = JAVA_DIR
    if JAVA_DIR is None:
        java_dir = os.environ.get("JAVA_HOME", None)
    if java_dir is None:
        warnings.warn("JAVA_DIR not set")
        return None
    jdk_folders = os.listdir(java_dir)
    if not jdk_folders:
        return None
    if len(jdk_folders) > 1:
        jdk_folders.sort()
        jdk_folders.reverse()
    # print(f"jdk_folders: {jdk_folders}")
    base_java_dir = os.path.join(java_dir, jdk_folders[0])
    if "linux" in sys.platform:
        return base_java_dir
    if "darwin" in sys.platform:
        return os.path.join(base_java_dir, "Contents", "Home")
    # if sys.platform == "darwin":
    #    return os.path.join(base_java_dir, "Contents", "Home", "bin")
    # return os.path.join(base_java_dir, "bin")
    return base_java_dir


def main(argv: list[str] | None = None) -> int:
    """Main"""
    # print(f"Java dir: {JAVA_DIR}")
    # print(os.listdir(JAVA_DIR))
    # print_tree_dir(JAVA_DIR, max_level=5)
    java_home = find_default_path_or_none()
    if java_home is None:
        warnings.warn("Java home not found")
        return 1
    java_exe = find_java_exe(java_home)
    # print(f"Java home: {java_home}")
    # print(f"Java exe: {java_exe}")
    os.environ["JAVA_HOME"] = java_home
    # print(f"Searched for bin directory and found: {java_exe}")
    # print(f"JAVA_HOME: {java_home}")
    rtn = trampoline(COMMAND, args=argv, default_path=java_exe)
    return rtn


if __name__ == "__main__":
    sys.exit(main())
