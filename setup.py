# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='quail',
    version='0.1.1',
    description='A python toolbox for analyzing and plotting free recall data',
    long_description=readme,
    author='Contextual Dynamics Lab',
    author_email='contextualdynamics@gmail.com',
    url='https://github.com/ContextLab/quail',
    license=license,
    packages=find_packages(exclude=('tests', 'docs', 'paper')),
    include_package_data=True,
    install_requires=[
        "seaborn>=0.7.1",
        "matplotlib>=1.5.1",
        "scipy>=0.17.1",
        "numpy>=1.10.4",
        "pandas>=0.20.3",
        "sqlalchemy",
        "dill",
        "requests",
        "pydub",
        "google-cloud-speech",
        "multiprocessing",
        "pathos",
        "future"
    ]
)
