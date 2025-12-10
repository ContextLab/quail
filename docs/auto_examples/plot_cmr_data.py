# -*- coding: utf-8 -*-
"""
=============================
Analyze Polyn et al. (2009) CMR Data
=============================

This example demonstrates analyzing the Polyn et al. (2009) free recall dataset,
which was used in the development of the Context Maintenance and Retrieval (CMR)
model. The dataset contains behavioral data from 45 subjects who studied lists
of 24 words using either SIZE or ANIMACY encoding tasks.

The experiment included three list types:
- Control (Size): All items studied using the SIZE task
- Control (Animacy): All items studied using the ANIMACY task
- Shift: Items alternated between SIZE and ANIMACY encoding tasks

We'll analyze recall performance using:
1. Probability of First Recall (PFR) - probability of recalling each position first
2. Lag-CRP - conditional recall probability by temporal lag
3. Serial Position Curve (SPC) - recall probability by encoding position
4. Memory Fingerprint - clustering by task and temporal features

Reference:
Polyn, S.M., Norman, K.A., & Kahana, M.J. (2009). A Context Maintenance and
Retrieval Model of Organizational Processes in Free Recall. Psychological
Review, Vol. 116 (1), 129-156. https://doi.org/10.1037/a0014420

"""

# Code source: Contextual Dynamics Laboratory
# License: MIT

from collections import Counter

import quail
import matplotlib.pyplot as plt
import warnings

# Suppress RuntimeWarnings about empty slices (from subjects with fewer lists)
warnings.filterwarnings('ignore', category=RuntimeWarning)

# Load the CMR dataset
egg = quail.load_example_data('cmr')

print(f"Loaded CMR data: {egg.n_subjects} subjects, {egg.n_lists} lists, "
      f"{egg.list_length} items per list")

# Build per-subject listgroups: map each list to its condition
# In this dataset, lists are mixed within subjects (each list has its own condition)
# Use None for lists without valid condition data (they will be excluded from grouped analyses)
listgroup = []
for subj_idx in range(egg.n_subjects):
    subj_listgroup = []
    for list_idx in range(egg.n_lists):
        try:
            sample = egg.pres.loc[(subj_idx, list_idx)][0]
            if sample and 'condition' in sample:
                subj_listgroup.append(sample['condition'])
            else:
                # Use the same group name as valid lists to avoid separate "Unknown" category
                # These are likely practice/buffer lists
                subj_listgroup.append(None)
        except (KeyError, IndexError, TypeError):
            subj_listgroup.append(None)
    listgroup.append(subj_listgroup)

# Count lists per condition (excluding None)
all_conditions = [c for subj in listgroup for c in subj if c is not None]
print(f"Lists per condition: {dict(Counter(all_conditions))}")

# Create a figure with subplots for each analysis
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# 1. Probability of First Recall - use quail's built-in plot with error bars
pfr = egg.analyze('pfr', listgroup=listgroup)
pfr.plot(ax=axes[0, 0], plot_type='list', legend=True)

# 2. Lag-CRP - use quail's built-in plot with error bars (legend=False)
lagcrp = egg.analyze('lagcrp', listgroup=listgroup)
lagcrp.plot(ax=axes[0, 1], plot_type='list', legend=False)

# 3. Serial Position Curve - use quail's built-in plot with error bars (legend=False)
spc = egg.analyze('spc', listgroup=listgroup)
spc.plot(ax=axes[1, 0], plot_type='list', legend=False)

# Configure PFR plot
axes[0, 0].set_title('Probability of First Recall')
axes[0, 0].set_xlabel('Serial Position')
axes[0, 0].set_ylabel('Probability')
axes[0, 0].set_ylim([0, 0.3])

# Configure Lag-CRP plot
axes[0, 1].set_title('Lag-CRP')
axes[0, 1].set_xlabel('Lag')
axes[0, 1].set_ylabel('Conditional Recall Probability')
axes[0, 1].set_xlim([-10, 10])
axes[0, 1].axvline(x=0, color='gray', linestyle='--', alpha=0.5)

# Configure SPC plot
axes[1, 0].set_title('Serial Position Curve')
axes[1, 0].set_xlabel('Serial Position')
axes[1, 0].set_ylabel('Recall Probability')
axes[1, 0].set_ylim([0, 1])

# 4. Memory Fingerprint - averaged across all lists
avg_listgroup = ['average'] * egg.n_lists
fingerprint = egg.analyze('fingerprint', features=['task', 'temporal'],
                          listgroup=avg_listgroup)
fingerprint.plot(ax=axes[1, 1], title='Memory Fingerprint', ylim=[0, 1])
axes[1, 1].set_xlabel('Feature')
axes[1, 1].set_ylabel('Clustering Score')

plt.tight_layout()
plt.suptitle('Polyn et al. (2009) CMR Dataset Analysis', y=1.02, fontsize=14)
plt.savefig('cmr_analysis.png', dpi=150, bbox_inches='tight')
plt.show()

print("\nAnalysis complete! Saved plot to cmr_analysis.png")
