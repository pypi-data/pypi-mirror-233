"""Setup for pypechain command line tool."""

from setuptools import find_packages, setup

setup(
    name="pypechain",
    version="0.0.0",
    packages=find_packages(),
    install_requires=["web3", "jinja2", "black"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": [
            "pypechain = mypackage.main:main",
        ],
    },
)
