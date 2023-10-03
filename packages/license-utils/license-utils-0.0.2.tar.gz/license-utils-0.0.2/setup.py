import os

from setuptools import find_packages, setup

_ROOT = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(_ROOT, "README.md")) as f:
    LONG_DESCRIPTION = f.read()


# Taken from: https://packaging.python.org/en/latest/guides/single-sourcing-package-version/#single-sourcing-the-package-version
# TODO replace this once transitioned to pyproject.toml, as described in the above link
def get_version(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(here, rel_path), "r") as fp:
        init_file = fp.read()

    for line in init_file.splitlines():
        if line.startswith("__version__"):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")


setup(
    name="license-utils",
    version=get_version("license_utils/__init__.py"),
    description="Various utilities for working with SPDX / OSS licenses, including a spdx-based license matcher.",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    author="Michael Weiss",
    url="https://github.com/miweiss/license-utils",
    packages=find_packages(exclude=["tests*"]),
    install_requires=["aiohttp>=3.8.5", "requests>=2.31.0", "nest_asyncio>=1.5.8"],
    license="MIT",
    extras_require={
        "test": [
            "pytest",
            "pytest-asyncio",
        ],
        "lint": [
            "black==23.3.0",
            "isort==5.12.0",
            "docstr-coverage==2.2.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "spdx-license-matcher = spdx_license_matcher.matcher:matcher"
        ]
    },
    keywords="spdx license license-matcher",
    classifiers=[        
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
