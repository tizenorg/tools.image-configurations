#!/bin/bash

if [ -z "$1" ]; then
	echo "Merge request number needed"
	exit 1
fi

# Check out a new branch for integration
git checkout -b merge-requests/$1

# Fetch the merge request into this branch
git pull git://gitorious.org:meego-os-base/image-configurations.git  refs/merge-requests/$1

# Show the commits, assess they are okay
git log --pretty=oneline --abbrev-commit master..merge-requests/$1

# To apply the changes to your branch:
git checkout master
git merge merge-requests/$1
git push origin master
