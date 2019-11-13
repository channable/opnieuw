import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="opnieuw",
    version="0.0.1",
    author="Channable",
    author_email="ruud@channable.com",
    description="Retries for humans",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/channable/opnieuw",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
