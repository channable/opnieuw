import setuptools
from retry import __version__

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="channable-retry",
    version=__version__,
    author="Channable",
    author_email="ruud@channable.com",
    description="Retries for humans",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/channable/workingtitle-retry",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
