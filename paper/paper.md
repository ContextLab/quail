---
title: 'Quail: A python toolbox for analyzing and plotting free recall data'
tags:
  - memory
  - free recall
  - python
authors:
 - name: Andrew C. Heusser
   orcid: 0
   affiliation: 1
 - name: Paxton C. Fitzpatrick
   orcid: 0
   affiliation: 1
 - name: Campbell E. Field
   orcid: 0
   affiliation: 1
 - name: Kirsten Ziman
   orcid: 0
   affiliation: 1
 - name: Jeremy R. Manning
   orcid: 0
   affiliation: 1
affiliations:
 - name: Department of Psychological and Brain Sciences, Dartmouth College
   index: 1
date: 31 August 2017
bibliography: paper.bib
---

# Summary

Quail is a Python package that facilitates analyzes of behavioral data from memory experiments. (The current focus is on free recall experiments.) Key features include:

- Serial position curves (probability of recalling items presented at each presentation position)
- Probability of Nth recall curves (probability of recalling items at each presentation position as the Nth recall in the recall sequence)
- Lag-Conditional Response Probability curves (probability of transitioning between items in the recall sequence, as a function of their relative presentation positions)
- Clustering metrics (e.g. single-number summaries of how often participants transition from recalling a word to another related word, where "related" can be user-defined.)
- Many nice plotting functions
- Convenience functions for loading in data
- Automatically parse speech data (audio files) using wrappers for the Google Cloud Speech to Text API

The toolbox name is inspired by Douglas Quail, the main character from the Philip K. Dick short story We Can Remember It for You Wholesale (the inspiration for the film Total Recall).

<!-- Citations to entries in paper.bib should be in
[rMarkdown](http://rmarkdown.rstudio.com/authoring_bibliographies_and_citations.html)
format.

Figures can be included like this: ![Fidgit deposited in figshare.](figshare_article.png) -->

<!-- # References -->
