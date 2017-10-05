# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='quail',
    version='0.1.3',
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
