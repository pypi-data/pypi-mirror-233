#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='pypremod',
    description='Python package for Premod solver',
    url='https://www.sintef.no',
    install_requires=[
        'numpy',
        'pandas',
        'pytest',
        'scipy',
        'matplotlib',
        'pypremod-calm==0.1.2',
        'pypremod-strength==0.1.6'
    ],
    version='0.1.5',
    packages=find_packages(),
    package_data={
        'premod': ['default/*.txt']
    }
)

