#!/usr/bin/env python

import os
from setuptools import setup, find_packages

def read(file_name):
    with open(os.path.join(os.path.dirname(__file__), file_name), encoding="utf-8") as f:
        return f.read()

setup(
    name="semrun",
    version="0.0.2",
    description="PigeonAI client and SDK",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    author="Aria Attar",
    author_email="aria.attar@gmail.com",
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=read("requirements.txt"),
    include_package_data=True,
    python_requires=">=3.6",
)