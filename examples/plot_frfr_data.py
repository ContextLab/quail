# -*- coding: utf-8 -*-
"""
=============================
Analyze Feature-Rich Free Recall (FRFR) Data
=============================

This example demonstrates analyzing the Feature-Rich Free Recall (FRFR) dataset,
which investigates how different word features affect memory organization during
free recall. The dataset contains 452 subjects across 11 experimental conditions,
each varying which word features were made salient during encoding.

Experimental conditions:
- feature-rich: All features varied (color, location, category, size, etc.)
- category: Only category information varied
- color: Only color information varied
- length: Only word length varied
- first-letter: Only first letter varied
- location: Only spatial location varied
- size: Only semantic size varied
- adaptive: Features adapted based on participant performance
- reduced: Minimal feature variation
- reduced-early: Reduced features in early lists
- reduced-late: Reduced features in late lists

Each subject studied 16 lists of 16 words. Lists 1-8 are considered "early" lists
and lists 9-16 are considered "late" lists.

We'll analyze recall performance using:
1. Serial Position Curve (SPC) - recall probability by encoding position
2. Probability of First Recall (PFR) - probability of recalling each position first
3. Lag-CRP - conditional recall probability by temporal lag
4. Memory Fingerprint - clustering by multiple features

Reference:
Heusser, A.C., Fitzpatrick, P.C., & Manning, J.R. (2018). How is experience
transformed into memory? bioRxiv. https://doi.org/10.1101/409987

"""

# Code source: Contextual Dynamics Laboratory
# License: MIT

from collections import Counter

import quail
import matplotlib.pyplot as plt
import warnings

# Suppress RuntimeWarnings about empty slices
warnings.filterwarnings('ignore', category=RuntimeWarning)

# Load the FRFR dataset
egg = quail.load_example_data('frfr')

print(f"Loaded FRFR data: {egg.n_subjects} subjects, {egg.n_lists} lists, "
      f"{egg.list_length} items per list")

# Build subjgroup: map each subject to its experimental condition
subjgroup = []
for subj_idx in range(egg.n_subjects):
    try:
        sample = egg.pres.loc[(subj_idx, 0)][0]
        if sample and 'condition' in sample:
            subjgroup.append(sample['condition'])
        else:
            subjgroup.append('unknown')
    except (KeyError, IndexError, TypeError):
        subjgroup.append('unknown')

# Count subjects per condition
condition_counts = Counter(subjgroup)
print("\nSubjects per condition:")
for cond, count in sorted(condition_counts.items()):
    print(f"  {cond}: {count}")

# Build per-subject listgroups: early (lists 0-7) vs late (lists 8-15)
# Each subject has their own listgroup since we want to compare early vs late
# within each condition
listgroup = []
for subj_idx in range(egg.n_subjects):
    subj_listgroup = []
    for list_idx in range(egg.n_lists):
        if list_idx < 8:
            subj_listgroup.append('early')
        else:
            subj_listgroup.append('late')
    listgroup.append(subj_listgroup)

# Create a listgroup for averaging all lists together (for fingerprint)
listgroup_average = ['average'] * egg.n_lists

# Create figure with 2x2 subplots
fig, axes = plt.subplots(2, 2, figsize=(14, 12))

# 1. Serial Position Curve - by condition, colored by early/late
print("\nAnalyzing Serial Position Curves...")
spc = egg.analyze('spc', listgroup=listgroup)
spc.plot(ax=axes[0, 0], subjgroup=subjgroup, plot_type='subject', legend=True)
axes[0, 0].set_title('Serial Position Curve by Condition (Early vs Late)')
axes[0, 0].set_xlabel('Serial Position')
axes[0, 0].set_ylabel('Recall Probability')
axes[0, 0].set_ylim([0, 1])
# Move legend outside plot
axes[0, 0].legend(loc='upper right', fontsize=7, ncol=2)

# 2. Probability of First Recall - by condition, early/late
print("Analyzing Probability of First Recall...")
pfr = egg.analyze('pfr', listgroup=listgroup)
pfr.plot(ax=axes[0, 1], subjgroup=subjgroup, plot_type='subject', legend=False)
axes[0, 1].set_title('Probability of First Recall by Condition')
axes[0, 1].set_xlabel('Serial Position')
axes[0, 1].set_ylabel('Probability')
axes[0, 1].set_ylim([0, 0.25])

# 3. Lag-CRP - by condition, early/late
print("Analyzing Lag-CRP...")
lagcrp = egg.analyze('lagcrp', listgroup=listgroup)
lagcrp.plot(ax=axes[1, 0], subjgroup=subjgroup, plot_type='subject', legend=False)
axes[1, 0].set_title('Lag-CRP by Condition')
axes[1, 0].set_xlabel('Lag')
axes[1, 0].set_ylabel('Conditional Recall Probability')
axes[1, 0].set_xlim([-10, 10])
axes[1, 0].axvline(x=0, color='gray', linestyle='--', alpha=0.5)

# 4. Memory Fingerprint - by available features
# Note: color and location are list-type features that require special handling
print("Analyzing Memory Fingerprints...")
fingerprint_features = ['category', 'size', 'wordLength', 'firstLetter', 'temporal']
fingerprint = egg.analyze('fingerprint', features=fingerprint_features,
                          listgroup=listgroup_average)
fingerprint.plot(ax=axes[1, 1], subjgroup=subjgroup, plot_type='subject',
                 title='Memory Fingerprint by Condition', ylim=[0, 1])
axes[1, 1].set_xlabel('Feature')
axes[1, 1].set_ylabel('Clustering Score')
# No legend here since we already have one in SPC plot

plt.tight_layout()
plt.suptitle('Feature-Rich Free Recall (FRFR) Dataset Analysis', y=1.02, fontsize=14)
plt.savefig('frfr_analysis.png', dpi=150, bbox_inches='tight')
plt.show()

print("\nAnalysis complete! Saved plot to frfr_analysis.png")
