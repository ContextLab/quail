---
title: 'Quail: A Python toolbox for analyzing and plotting free recall data'
tags:
 - memory
 - free recall
 - python
 - visualization
authors:
 - name: Andrew C. Heusser
   orcid: 0000-0001-6353-688X
   affiliation: 1
 - name: Paxton C. Fitzpatrick
   orcid: 0000-0003-0205-3088
   affiliation: 1
 - name: Campbell E. Field
   orcid: 0000-0001-7260-635X
   affiliation: 1
 - name: Kirsten Ziman
   orcid: 0000-0002-8942-3362
   affiliation: 1
 - name: Jeremy R. Manning
   orcid: 0000-0001-7613-4732
   affiliation: 1
affiliations:
 - name: Department of Psychological and Brain Sciences, Dartmouth College
   index: 1
date: 31 August 2017
bibliography: paper.bib
---

# Summary
Quail [@quail_code] is a Python package for analyzing and plotting behavioral data from memory experiments. (The current focus is on free recall experiments [@Kaha12, @MannEtal15].) Quail implements classic and more recently developed memory analyses and provides easy plotting functions by wrapping Seaborn [@WaskEtAl16]. API documentation, tutorials and examples can be found on our readthedocs page [@quail_docs]. Key features include:

- Creating and plotting serial position curves (probability of recalling items presented at each presentation position) [@Ebbi85, @Murd62a]
- Creating and plotting probability of *N*th recall curves (probability of recalling items at each presentation position as the *N*th recall in the recall sequence) [@Hoga75]
- Creating and plotting lag-Conditional Response Probability curves (probability of transitioning between items in the recall sequence, as a function of their relative presentation positions) [@Kaha96]
- Computing clustering metrics (e.g. single-number summaries of how often participants transition from recalling a word to another related word, where "related" can be user-defined; [@Kaha12, @MannEtal15])
- Many nice additional plotting functions
- Convenience functions for loading and saving data
- Wrapper functions for automatically transcribing speech data (audio files) using the [Google Cloud Speech-to-Text API](https://cloud.google.com/speech/)

The intended user of this toolbox is a memory researcher who seeks an easy way to analyze and visualize data from free recall psychology experiments.

The toolbox name is inspired by Douglas Quail, the main character from the Philip K. Dick short story [*We Can Remember It for You Wholesale*](https://en.wikipedia.org/wiki/We_Can_Remember_It_for_You_Wholesale) (the inspiration for the film [*Total Recall*](https://en.wikipedia.org/wiki/Total_Recall_(1990_film))).

# References
