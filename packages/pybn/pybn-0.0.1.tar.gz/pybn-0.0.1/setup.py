#!/usr/bin/env python3

from setuptools import setup
from pathlib import Path

setup(
    name='pybn',
    version='0.0.1',
    py_modules=['pybn'],
    license='MIT',
    description='Python package for simple build number generation.',
    long_description=(Path(__file__).parent / "README.md").read_text(),
    long_description_content_type='text/markdown',
    url='https://github.com/CodeConfidant/pybn',
    author='Drew Hainer',
    author_email='codeconfidant@gmail.com',
    platforms=['Windows', 'Linux']
)

# - Update README.md
# - Update Version Number
# - Tar Wrap the Package: python setup.py sdist
# - Check Package: twine check dist/*
# - Upload to PYPI: twine upload dist/* -u <username> -p <password>
# - Commit Changes
# - Change Release Version in Github Repo