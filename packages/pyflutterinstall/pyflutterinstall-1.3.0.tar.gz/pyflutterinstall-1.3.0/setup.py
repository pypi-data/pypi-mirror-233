import os
import re

import setuptools

URL = "https://github.com/zackees/pyflutterinstall"

# The directory containing this file
HERE = os.path.dirname(__file__)

def get_readme() -> str:
    """Get the contents of the README file."""
    readme = os.path.join(HERE, "README.md")
    with open(readme, encoding="utf-8", mode="r") as readme_file:
        readme_lines = readme_file.readlines()
    for i, line in enumerate(readme_lines):
        if "../../" in line:
            # Transform the relative links to absolute links
            output_string = re.sub(r"(\.\./\.\.)", f"{URL}", line, count=1)
            output_string = re.sub(r"(\.\./\.\.)", f"{URL}", output_string)
            readme_lines[i] = output_string
    return "".join(readme_lines)


if __name__ == "__main__":
    setuptools.setup(
        long_description=get_readme(),
        long_description_content_type="text/markdown",
        url=URL,
        include_package_data=True,
        extras_require={
            'test': ['pytest', 'pytest-cov'],
        },
        entry_points={
            "console_scripts": [
                "pyflutterinstall = pyflutterinstall.cli:main",
                "pyflutteractivate = pyflutterinstall.setenv:init_dotenv",
                "pyflutterprintconfig = pyflutterinstall.config:print_config",
                "sdkmanager = pyflutterinstall.cmds.sdkmanager:main",
                "avdmanager = pyflutterinstall.cmds.avdmanager:main",
                "adb = pyflutterinstall.cmds.adb:main",
                "gradle = pyflutterinstall.cmds.gradle:main",
                "emulator = pyflutterinstall.cmds.emulator:main",
                "java = pyflutterinstall.cmds.java:main",
                "apkanalyzer = pyflutterinstall.cmds.apkanalyzer:main",
            ],
        },
    )
