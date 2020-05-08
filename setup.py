# Opnieuw: Retries for humans
# Copyright 2019 Channable
#
# Licensed under the 3-clause BSD license, see the LICENSE file in the repository root.

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

__version__ = "1.1.0"

setuptools.setup(
    name="opnieuw",
    version=__version__,
    author="Channable",
    author_email="ruud@channable.com",
    description="Retries for humans",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/channable/opnieuw",
    packages=setuptools.find_packages(exclude=('tests',)),
    package_data={
        'opnieuw': ['py.typed'],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
