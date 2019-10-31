import setuptools
from retry import  __version__

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="example-pkg-your-username",
    version=__version__,
    author="Channable",
    author_email="info@channable.com",
    description="Retries for humans” tagline",
    long_description=open('README.rst').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: 3-clause BSD.",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
