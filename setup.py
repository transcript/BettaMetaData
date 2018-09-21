#!/usr/bin/env python
from setuptools import setup, find_packages
__author__ = 'adamkoziol'
setup(
    name="BettaMetadata",
    version="0.0.04",
    include_package_data=True,
    packages=find_packages(),
    scripts=['validator.py'],
    license='GPL-3.0',
    author='Adam Koziol',
    author_email='adam.koziol@canada.ca',
    description='Better metadata for BioSamples',
    url='https://github.com/transcript/BettaMetaData',
    long_description=open('README.md').read()
)
