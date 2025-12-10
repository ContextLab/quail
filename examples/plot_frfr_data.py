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
1. Probability of First Recall (PFR) - probability of recalling each position first
2. Lag-CRP - conditional recall probability by temporal lag
3. Serial Position Curve (SPC) - recall probability by encoding position
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
import seaborn as sns
import warnings

# Suppress RuntimeWarnings about empty slices
warnings.filterwarnings('ignore', category=RuntimeWarning)

# Create viridis palette for distinguishing 11 conditions
viridis_palette = sns.color_palette("viridis", n_colors=11)

# Load the FRFR dataset
egg = quail.load_example_data('frfr')

print(f"Loaded FRFR data: {egg.n_subjects} subjects, {egg.n_lists} lists, "
      f"{egg.list_length} items per list")

# Build subjgroup: map each subject to its experimental condition
subjgroup = []
for subj_idx in range(egg.n_subjects):
    try:
        sample = egg.pres.loc[(subj_idx, 0)][0]
        if sample and 'Condition' in sample:
            subjgroup.append(sample['Condition'])
        else:
            subjgroup.append('Unknown')
    except (KeyError, IndexError, TypeError):
        subjgroup.append('Unknown')

# Define condition order for consistent plotting
condition_order = [
    'Feature rich',
    'Reduced early',
    'Reduced late',
    'Reduced',
    'Adaptive',
    'Category',
    'Size',
    'Color',
    'Location',
    'Word length',
    'First letter'
]

# Count subjects per condition
condition_counts = Counter(subjgroup)
print("\nSubjects per condition:")
for cond in condition_order:
    if cond in condition_counts:
        print(f"  {cond}: {condition_counts[cond]}")

# Split egg into early (lists 0-7) and late (lists 8-15) lists
print("\nSplitting data into early and late lists...")
egg_early = egg.crack(lists=list(range(8)))
egg_late = egg.crack(lists=list(range(8, 16)))

print(f"Early lists egg: {egg_early.n_subjects} subjects, {egg_early.n_lists} lists")
print(f"Late lists egg: {egg_late.n_subjects} subjects, {egg_late.n_lists} lists")

# Create listgroup for averaging across lists within each split
listgroup_early = ['average'] * egg_early.n_lists
listgroup_late = ['average'] * egg_late.n_lists

# ============================================================================
# Figure 1: PFR, Lag-CRP, SPC for Early (top) and Late (bottom) lists
# ============================================================================
print("\n" + "=" * 60)
print("Creating Figure 1: PFR, Lag-CRP, SPC by condition")
print("=" * 60)

fig1, axes1 = plt.subplots(2, 3, figsize=(18, 10), sharey='col')

# --- Top row: Early lists ---
print("\nAnalyzing early lists...")

# PFR - Early
print("  Computing PFR (early)...")
pfr_early = egg_early.analyze('pfr', listgroup=listgroup_early)
pfr_early.plot(ax=axes1[0, 0], subjgroup=subjgroup, plot_type='subject', legend=True,
               hue_order=condition_order, palette=viridis_palette)
axes1[0, 0].set_title('Probability of First Recall (Early Lists)')
axes1[0, 0].set_xlabel('Serial Position')
axes1[0, 0].set_ylabel('Probability')
axes1[0, 0].set_ylim([0, 0.3])
axes1[0, 0].legend(loc='upper right', fontsize=6, ncol=2)

# Lag-CRP - Early
print("  Computing Lag-CRP (early)...")
lagcrp_early = egg_early.analyze('lagcrp', listgroup=listgroup_early)
lagcrp_early.plot(ax=axes1[0, 1], subjgroup=subjgroup, plot_type='subject', legend=False,
                  hue_order=condition_order, palette=viridis_palette)
axes1[0, 1].set_title('Lag-CRP (Early Lists)')
axes1[0, 1].set_xlabel('Lag')
axes1[0, 1].set_ylabel('Conditional Recall Probability')
axes1[0, 1].set_xlim([-10, 10])
axes1[0, 1].axvline(x=0, color='gray', linestyle='--', alpha=0.5)

# SPC - Early
print("  Computing SPC (early)...")
spc_early = egg_early.analyze('spc', listgroup=listgroup_early)
spc_early.plot(ax=axes1[0, 2], subjgroup=subjgroup, plot_type='subject', legend=False,
               hue_order=condition_order, palette=viridis_palette)
axes1[0, 2].set_title('Serial Position Curve (Early Lists)')
axes1[0, 2].set_xlabel('Serial Position')
axes1[0, 2].set_ylabel('Recall Probability')
axes1[0, 2].set_ylim([0, 1])

# --- Bottom row: Late lists ---
print("\nAnalyzing late lists...")

# PFR - Late
print("  Computing PFR (late)...")
pfr_late = egg_late.analyze('pfr', listgroup=listgroup_late)
pfr_late.plot(ax=axes1[1, 0], subjgroup=subjgroup, plot_type='subject', legend=False,
              hue_order=condition_order, palette=viridis_palette)
axes1[1, 0].set_title('Probability of First Recall (Late Lists)')
axes1[1, 0].set_xlabel('Serial Position')
axes1[1, 0].set_ylabel('Probability')
axes1[1, 0].set_ylim([0, 0.3])

# Lag-CRP - Late
print("  Computing Lag-CRP (late)...")
lagcrp_late = egg_late.analyze('lagcrp', listgroup=listgroup_late)
lagcrp_late.plot(ax=axes1[1, 1], subjgroup=subjgroup, plot_type='subject', legend=False,
                 hue_order=condition_order, palette=viridis_palette)
axes1[1, 1].set_title('Lag-CRP (Late Lists)')
axes1[1, 1].set_xlabel('Lag')
axes1[1, 1].set_ylabel('Conditional Recall Probability')
axes1[1, 1].set_xlim([-10, 10])
axes1[1, 1].axvline(x=0, color='gray', linestyle='--', alpha=0.5)

# SPC - Late
print("  Computing SPC (late)...")
spc_late = egg_late.analyze('spc', listgroup=listgroup_late)
spc_late.plot(ax=axes1[1, 2], subjgroup=subjgroup, plot_type='subject', legend=False,
              hue_order=condition_order, palette=viridis_palette)
axes1[1, 2].set_title('Serial Position Curve (Late Lists)')
axes1[1, 2].set_xlabel('Serial Position')
axes1[1, 2].set_ylabel('Recall Probability')
axes1[1, 2].set_ylim([0, 1])

plt.tight_layout()
fig1.suptitle('FRFR Dataset: Recall Analyses by Condition (Early vs Late Lists)',
              y=1.02, fontsize=14)
plt.savefig('frfr_recall_analysis.png', dpi=150, bbox_inches='tight')
print("\nSaved Figure 1 to frfr_recall_analysis.png")

# ============================================================================
# Figure 2: Memory Fingerprints for Early (top) and Late (bottom) lists
# ============================================================================
print("\n" + "=" * 60)
print("Creating Figure 2: Memory Fingerprints by condition")
print("=" * 60)

# Stacked layout: 2 rows, 1 column (larger to avoid overlapping text)
fig2, axes2 = plt.subplots(2, 1, figsize=(8, 8), sharey=True)

# Features for fingerprint analysis (sentence case)
fingerprint_features = ['Category', 'Size', 'Color', 'Location',
                        'Word length', 'First letter', 'Temporal']

# Fingerprint - Early lists (top panel)
print("\nComputing fingerprints (early lists)...")
fp_early = egg_early.analyze('fingerprint', features=fingerprint_features,
                             listgroup=listgroup_early)
fp_early.plot(ax=axes2[0], subjgroup=subjgroup, plot_type='subject',
              plot_style='bar', ylim=[0.5, 0.81], legend=False,
              hue_order=condition_order, palette=viridis_palette)
axes2[0].set_title('Memory fingerprints\nEarly lists', fontsize=14)
axes2[0].set_xlabel('')  # Remove x-label on top panel
axes2[0].set_ylabel('Clustering score', fontsize=14)
axes2[0].tick_params(axis='x', labelbottom=False)  # Hide x tick labels on top

# Fingerprint - Late lists (bottom panel)
print("Computing fingerprints (late lists)...")
fp_late = egg_late.analyze('fingerprint', features=fingerprint_features,
                           listgroup=listgroup_late)
fp_late.plot(ax=axes2[1], subjgroup=subjgroup, plot_type='subject',
             plot_style='bar', ylim=[0.5, 0.81], legend=True,
             hue_order=condition_order, palette=viridis_palette)
axes2[1].set_title('Late lists', fontsize=14)
axes2[1].set_xlabel('Feature', fontsize=14)
axes2[1].set_ylabel('Clustering score', fontsize=14)
# Move legend to upper right of bottom panel
axes2[1].legend(loc='upper right', fontsize=6, ncol=3, title='Condition')

plt.tight_layout()
plt.savefig('frfr_fingerprint_analysis.png', dpi=150, bbox_inches='tight')
print("Saved Figure 2 to frfr_fingerprint_analysis.png")

plt.show()

print("\nAnalysis complete!")
