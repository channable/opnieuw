import setuptools
from retry import __version__

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="channable-retry",
    version=__version__,
    author="Channable",
    author_email="ruud@channable.com",
    description="Retries for humans",
    long_description=open('README.rst').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/channable/workingtitle-retry",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: 3-clause BSD.",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
