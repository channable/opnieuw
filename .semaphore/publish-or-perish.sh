#!/bin/bash

# These commands are in a separate script so it can exit before
# it reaches the end of the file, without Semaphore thinking it
# has failed.

set -efuo pipefail

git fetch --tags
TAG=v$(python setup.py --version)
# If the tag already exist this command will fail and the job will exit
# without raising an error. Otherwise, we will build the project,
# publish to PyPi, and push the tag to github.
git tag "$TAG" || exit 0
sudo pip install twine
twine upload --skip-existing dist/*
git push origin "$TAG"
