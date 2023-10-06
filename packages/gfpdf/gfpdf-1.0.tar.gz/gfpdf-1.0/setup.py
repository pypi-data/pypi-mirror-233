from setuptools import setup, find_packages
from pathlib import Path

setup(
    name="gfpdf",
    version=1.0,
    long_description=Path("README.md").read_text(),
    packages=find_packages(exclude=["data", "tests"])
)
