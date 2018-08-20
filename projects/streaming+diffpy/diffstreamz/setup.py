#!/usr/bin/env python

from os.path import exists
from setuptools import setup, find_packages


setup(
    name="diffstreamz",
    version='0.1.0',
    description="Streams",
    url="https://github.com/ecacomsig/Mieres-2018/tree/master/projects/streaming%2Bdiffpy/diffstreamz",
    maintainer="Simon Billinge",
    license="BSD",
    keywords="streams",
    packages=find_packages(),
    long_description=(
        open("README.md").read() if exists("README.md") else ""
    ),
    install_requires=list(open("requirements.txt").read().strip().split("\n")),
    zip_safe=False,
)
