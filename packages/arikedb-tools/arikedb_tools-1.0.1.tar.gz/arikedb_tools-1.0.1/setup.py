#!/usr/bin/python3
from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


with open('arikedb_tools/__init__.py', 'r') as f:
    version = list(
        filter(lambda line: "__version__ =" in line, f.readlines())
    )[0].split("\"")[1]

setup(
    name="arikedb_tools",
    version=version,
    description="Arikedb Python Tools",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Alejandro Alfonso",
    author_email="alejandroalfonso1994@gmail.com",
    url="https://gitlab.com/arikedb1/languages-library-support"
        "/tools/arikedb-python-tools",
    packages=find_packages(exclude=['tests', 'demo']),
    include_package_data=True,
    install_requires=[r.strip() for r in open("requirements.txt").readlines()]
)
