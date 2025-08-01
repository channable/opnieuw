#!/bin/bash

# These commands are in a separate script so it can exit before
# it reaches the end of the file, without Semaphore thinking it
# has failed.

set -efuo pipefail

sudo pip install toml
TAG=v$(grep -Po '__version__ = .\K[0-9\\.]+' opnieuw/__init__.py)
# If the tag already exist this command will fail and the job will exit
# without raising an error. Otherwise, we will build the project,
# publish to PyPi, and push the tag to github.
git fetch --tags
git tag "$TAG" || exit 0

sudo pip install build
python3 -m build

sudo pip install twine
python3 -m twine upload --skip-existing dist/*

git push origin "$TAG"
