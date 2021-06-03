[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.1003184.svg)](https://doi.org/10.5281/zenodo.1003184)
[![JOSS](http://joss.theoj.org/papers/3fb5123eb2538e06f6a25ded0a088b73/status.svg)](http://joss.theoj.org/papers/10.21105/joss.00424)

![Quail logo](images/Quail_Logo_small.png)

<h2>Overview</h2>

Quail is a Python package that facilitates analyses of behavioral data from memory experiments.  (The current focus is on free recall experiments.)  Key features include:
- Serial position curves (probability of recalling items presented at each presentation position)
- Probability of Nth recall curves (probability of recalling items at each presentation position as the Nth recall in the recall sequence)
- Lag-Conditional Response Probability curves (probability of transitioning between items in the recall sequence, as a function of their relative presentation positions)
- Clustering metrics (e.g. single-number summaries of how often participants transition from recalling a word to another related word, where "related" can be user-defined.)
- Many nice plotting functions
- Convenience functions for loading in data
- Automatically parse speech data (audio files) using wrappers for the Google Cloud Speech to Text API

The intended user of this toolbox is a memory researcher who seeks an easy way to analyze and visualize data from free recall psychology experiments.

The toolbox name is inspired by Douglas Quail, the main character from the Philip K. Dick short story [_We Can Remember It for You Wholesale_](https://en.wikipedia.org/wiki/We_Can_Remember_It_for_You_Wholesale) (the inspiration for the film [_Total Recall_](https://en.wikipedia.org/wiki/Total_Recall_(1990_film))).

<h2>Try it!</h2>

Check out our [repo](https://github.com/ContextLab/quail-example-notebooks) of Jupyter notebooks.

<!-- Click the badge to launch a binder instance with example uses:

[![Binder](http://mybinder.org/badge.svg)](http://mybinder.org:/repo/contextlab/quail-example-notebooks)

or -->

<h2>Installation</h2>

To install quail in the recommended way, run:

`pip install quail`

This will install quail with basic functionality.  To install with speech decoding dependencies (Note: you will still need to install ffmpeg manually on your computer since it is not pip installable. For instructions, see [here](http://cdl-quail.readthedocs.io/en/latest/tutorial/speech_decoding.html)):

`pip install quail[speech-decoding]`

For CDL users, you can install speech decoding and efficient learning capabilities like this:

`pip install quail[speech-decoding, efficient-learning]`

To install directly from this repo (not recommended, but you'll get the "bleeding edge" version of the code):

`git clone https://github.com/ContextLab/quail.git`

Then, navigate to the folder and type:

`pip install -e .`

(this assumes you have [pip](https://pip.pypa.io/en/stable/installing/) installed on your system)

This will work on clean systems, but if you encounter issues you may need to run:

`sudo pip install --upgrade --ignore-installed -e .`

<h2>Requirements</h2>

+ python>=3.6
+ pandas>=0.18.0
+ seaborn>=0.7.1
+ matplotlib>=1.5.1
+ scipy>=0.17.1
+ numpy>=1.10.4
+ future
+ pytest (for development)

If installing from github (instead of pip), you must also install the requirements:
`pip install -r requirements.txt`

<h2>Documentation</h2>

Check out our readthedocs: [here](http://cdl-quail.readthedocs.io/en/latest/).

We also have a repo with example notebooks from the paper [here](https://github.com/ContextLab/quail-example-notebooks).


<h2>Citing</h2>

Please cite as:

Heusser AC, Fitzpatrick PC, Field CE, Ziman K, Manning JR (2017) Quail: A Python toolbox for analyzing and plotting free recall data. _The Journal of Open Source Software_, _2_(18) https://doi.org/10.21105%2Fjoss.00424

Here is a bibtex formatted reference:

```
@ARTICLE {HeusEtal2017b,
	doi = {10.21105/joss.00424},
	url = {https://doi.org/10.21105%2Fjoss.00424},
	year = 2017,
	publisher = {The Open Journal},
	volume = {2},
	number = {18},
	author = {Andrew C. Heusser and Paxton C. Fitzpatrick and Campbell E. Field and Kirsten Ziman and Jeremy R. Manning},
	title = {Quail: A Python toolbox for analyzing and plotting free recall data},
	journal = {The Journal of Open Source Software}
}
```

<h2>Contributing</h2>

(Some text borrowed from Matplotlib contributing [guide](http://matplotlib.org/devdocs/devel/contributing.html).)

<h3>Submitting a bug report</h3>

If you are reporting a bug, please do your best to include the following:

1. A short, top-level summary of the bug. In most cases, this should be 1-2 sentences.
2. A short, self-contained code snippet to reproduce the bug, ideally allowing a simple copy and paste to reproduce. Please do your best to reduce the code snippet to the minimum required.
3. The actual outcome of the code snippet
4. The expected outcome of the code snippet

<h3>Contributing code</h3>

The preferred way to contribute to quail is to fork the main repository on GitHub, then submit a pull request.

+ If your pull request addresses an issue, please use the title to describe the issue and mention the issue number in the pull request description to ensure a link is created to the original issue.

+ All public methods should be documented on our [readthedocs](http://cdl-quail.readthedocs.io/en/latest/api.html) API page.

+ Each high-level plotting function should have a simple example in the examples folder. This should be as simple as possible to demonstrate the method.

+ Changes (both new features and bugfixes) should be tested using `pytest`.  Add tests for your new feature to the `tests/` repo folder.

<h2>Support</h2>

If you have a question, comment or concern about the software, please post a question to [Stack Overflow](https://stackoverflow.com/search?q=quail), or send us an email at contextualdynamics@gmail.com.

<h2>Testing</h2>

![Build Status](https://travis-ci.org/ContextLab/quail.svg?branch=master)


To test quail, install pytest (`pip install pytest`) and run `pytest` in the quail folder

<h2>Examples</h2>

See [here](http://cdl-quail.readthedocs.io/en/latest/auto_examples/index.html) for more examples.

<h2>Create an egg!</h2>

Eggs are the fundamental data structure in `quail`.  They are comprised of lists of presented words, lists of recalled words, and a few other optional components.

```
import quail

# presented words
presented_words = [['cat', 'bat', 'hat', 'goat'],['zoo', 'animal', 'zebra', 'horse']]

# recalled words
recalled_words = [['bat', 'cat', 'goat', 'hat'],['animal', 'horse', 'zoo']]

# create egg
egg = quail.Egg(pres=presented_words, rec=recalled_words)

```

<h2>Analyze some data</h2>

```
#load data
egg = quail.load_example_data()

#analysis
analyzed_data = quail.analyze(egg, analysis='accuracy', listgroup=['average']*8)
```

<h2>Plot Accuracy</h2>

```
analyzed_data = quail.analyze(egg, analysis='accuracy', listgroup=['average']*8)
ax = quail.plot(analyzed_data, title='Recall Accuracy')
```
![Plot Accuracy](images/plot_acc.png)

<h2>Plot Serial Position Curve</h2>

```
analyzed_data = quail.analyze(egg, analysis='spc', listgroup=['average']*8)
ax = quail.plot(analyzed_data, title='Serial Position Curve')
```
![Plot SPC](images/plot_spc.png)

<h2>Plot Probability of First Recall</h2>

```
analyzed_data = quail.analyze(egg, analysis='pfr', listgroup=['average']*8)
ax = quail.plot(analyzed_data, title='Probability of First Recall')
```
![Plot PFR](images/plot_pfr.png)

<h2>Plot Lag-CRP</h2>

```
analyzed_data = quail.analyze(egg, analysis='lagcrp', listgroup=['average']*8)
ax = quail.plot(analyzed_data, title='Lag-CRP')
```
![Plot Lag-CRP](images/plot_lagcrp.png)

<h2>Plot Memory Fingerprint</h2>

```
analyzed_data = quail.analyze(egg, analysis='fingerprint', listgroup=['average']*8)
ax = quail.plot(analyzed_data, title='Memory Fingerprint')
```
![Plot Fingerprint](images/plot_fingerprint.png)
