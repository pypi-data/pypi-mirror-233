"""
Command stub for sdkmanager
"""
import os
import sys
from pyflutterinstall.trampoline import trampoline
from pyflutterinstall.config import config_load

from pyflutterinstall.cmds.java import find_default_path_or_none

ANDROID_SDK = config_load().get("ANDROID_SDK", ".")
JAVA_DIR = config_load().get("JAVA_DIR", None)
if ANDROID_SDK != ".":
    os.environ["ANDROID_SDK"] = ANDROID_SDK
    os.environ["ANDROID_HOME"] = ANDROID_SDK

COMMAND = "sdkmanager"
DEFAULT_PATH = os.path.join(ANDROID_SDK, "cmdline-tools", "latest", "bin")


def main(argv: list[str] | None = None) -> int:
    """Main"""
    argv = argv or sys.argv[1:]
    has_sdk_root = False
    for arg in argv:
        if arg.startswith("--sdk_root"):
            has_sdk_root = True
            break
    if not has_sdk_root:
        argv.append(f"--sdk_root={ANDROID_SDK}")
    java_home = find_default_path_or_none()
    assert java_home is not None, "Java home not found"
    os.environ["JAVA_HOME"] = java_home
    return trampoline(COMMAND, args=argv, default_path=DEFAULT_PATH)


if __name__ == "__main__":
    sys.exit(main())
