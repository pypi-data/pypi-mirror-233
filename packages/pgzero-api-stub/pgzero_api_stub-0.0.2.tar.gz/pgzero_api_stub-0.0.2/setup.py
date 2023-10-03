#!python
# -*- coding:utf-8 -*-
from __future__ import print_function
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="pgzero_api_stub",
    version='0.0.2',
    author="liushengkun",
    author_email="allan@163.com",
    description="a stub for pgzero",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    url="https://github.com/xxNull-lsk/pgzero_api_stub",
    packages=['pgzero_api_stub'],
    install_requires=[
        "pgzero <= 1.2.1"
        ],
    classifiers=[
        "Topic :: Games/Entertainment ",
        'Topic :: Games/Entertainment :: Puzzle Games',
        'Topic :: Games/Entertainment :: Board Games',
        "Topic :: Software Development :: Libraries :: Python Modules",
        'Programming Language :: Python :: 3 :: Only'
    ],
)

