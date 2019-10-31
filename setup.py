import setuptools
import os


with open(os.path.join(os.path.dirname(__file__), 'channable_retry/VERSION'), 'rb') as f:
    version = f.read().decode('ascii').strip()

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="example-pkg-your-username",
    version=version,
    author="Channable",
    author_email="info@channable.com",
    description="Retries for humans” tagline",
    long_description=open('README.rst').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'Twisted>=16.0.0;python_version=="2.7"',
    ],
)
