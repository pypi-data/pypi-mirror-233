import os
from setuptools import setup, find_namespace_packages
from pathlib import Path


this_directory = Path(__file__).parent

setup(
    name="traxix.trixli",
    version="0.1.0",
    url="https://gitlab.com/trax/trixli",
    packages=find_namespace_packages(include=["traxix.*"]),
    install_requires=(this_directory / "requirements.txt").read_text().splitlines(),
    scripts=[
        "traxix/trixli/again",
        "traxix/trixli/pexor.py",
        "traxix/trixli/fython",
        "traxix/trixli/f",
        "traxix/trixli/fr",
        "traxix/trixli/fp",
        "traxix/trixli/fe",
        "traxix/trixli/ec2l",
        "traxix/trixli/b64",
    ],
    author="trax Omar Givernaud",
    long_description=(this_directory / "README.md").read_text(),
    long_description_content_type="text/markdown",
)
