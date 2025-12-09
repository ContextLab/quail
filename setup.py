# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

DESCRIPTION = 'A python toolbox for analyzing and plotting free recall data'
LONG_DESCRIPTION = """\
Quail is a Python package that facilitates analyses of behavioral data from memory experiments. (The current focus is on free recall experiments.) Key features include:

- Serial position curves (probability of recalling items presented at each presentation position)
- Probability of Nth recall curves (probability of recalling items at each presentation position as the Nth recall in the recall sequence)
- Lag-Conditional Response Probability curves (probability of transitioning between items in the recall sequence, as a function of their relative presentation positions)
- Clustering metrics (e.g. single-number summaries of how often participants transition from recalling a word to another related word, where "related" can be user-defined.)
- Many nice plotting functions
- Convenience functions for loading in data
- Automatically parse speech data (audio files) using wrappers for the Google Cloud Speech to Text API

The intended user of this toolbox is a memory researcher who seeks an easy way to analyze and visualize data from free recall psychology experiments.
"""


EXTRAS_REQUIRE={
    'speech-decoding': ["pydub", "openai-whisper"],
    'efficient-learning': ["sqlalchemy"],
}

setup(
    name='quail',
    version='0.3.0',
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/x-rst',
    author='Contextual Dynamics Lab',
    author_email='contextualdynamics@gmail.com',
    url='https://github.com/ContextLab/quail',
    license='MIT',
    packages=find_packages(exclude=('tests', 'docs', 'paper')),
    include_package_data=True,
    install_requires=[
        'numpy>=2.0.0',
        'scipy>=1.10.0',
        'matplotlib>=3.5.0',
        'seaborn>=0.12.0',
        'pandas>=2.0.0',
        'joblib>=1.3.0',
    ],
    extras_require=EXTRAS_REQUIRE,
)
