# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='quail',
    version='0.2.0',
    description='A python toolbox for analyzing and plotting free recall data',
    long_description=' ',
    author='Contextual Dynamics Lab',
    author_email='contextualdynamics@gmail.com',
    url='https://github.com/ContextLab/quail',
    license='MIT',
    packages=find_packages(exclude=('tests', 'docs', 'paper')),
    include_package_data=True,
    install_requires=[
        "seaborn>=0.7.1",
        "matplotlib>=1.5.1",
        "scipy>=0.17.1",
        "numpy>=1.10.4",
        "pandas",
        "grpcio",
        "sqlalchemy",
        "dill",
        "requests",
        "pydub",
        "google-cloud-speech<0.31dev,>=0.30.0",
        "google-cloud>=0.32.0,<0.34.0",
        "pathos",
        "future",
        "six",
        "deepdish",
        "joblib",
    ]
)
