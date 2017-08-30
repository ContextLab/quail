# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='quail',
    version='0.1.0',
    description='A python toolbox for analyzing and plotting free recall data',
    long_description=readme,
    author='Contextual Dynamics Lab',
    author_email='contextualdynamics@gmail.com',
    url='https://github.com/ContextLab/quail',
    license=license,
    packages=find_packages(exclude=('tests', 'docs', 'paper')),
    include_package_data=True,
)
