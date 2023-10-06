# Opnieuw: Retries for humans
# Copyright 2019 Channable
#
# Licensed under the 3-clause BSD license, see the LICENSE file in the repository root.

import setuptools  # type: ignore

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

__version__ = "3.0.0"

setuptools.setup(
    name="opnieuw",
    version=__version__,
    author="Channable",
    author_email="ruud@channable.com",
    description="Retries for humans",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/channable/opnieuw",
    packages=setuptools.find_packages(exclude=("tests",)),
    package_data={
        "opnieuw": ["py.typed"],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: Implementation :: CPython",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Development Status :: 6 - Mature",
    ],
    python_requires=">=3.8",
    install_requires=[
        "typing-extensions>=3.10.0;python_version<'3.10'",
    ],
)
