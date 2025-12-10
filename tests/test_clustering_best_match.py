import pytest
import quail
import pandas as pd
import numpy as np
from quail.analysis.clustering import fingerprint_helper

def test_clustering_best_match():
    # Setup egg where "best" match logic differs from "exact"
    # "best" uses matchmat (dist) to find closest item even if not exact?
    # Actually _get_weight_best uses argmin of matchmat.
    # matchmat is distance between pres and rec features.
    # If standard features (exact matches possible), best == exact.
    # But if continuous features (e.g. color), exact fails.
    
    # Continuous feature: color (RGB)
    pres = [[['a', 'b', 'c']]]
    # For match='best', rec must have the feature values attached
    rec_feat = [{'item': 'a', 'color': [0.1]}, {'item': 'b', 'color': [0.5]}, {'item': 'c', 'color': [0.9]}]
    rec = [[rec_feat]]
    
    # features: 'color'
    # a: [0.1], b: [0.5], c: [0.9]
    features = [{'item': 'a', 'color': [0.1]}, {'item': 'b', 'color': [0.5]}, {'item': 'c', 'color': [0.9]}]
    pres_feat = [[features]] # 1 subj, 1 list
    # rec uses same items
    
    # But let's say recalled item has slightly DIFFERENT feature value? 
    # Quail usually assumes Recalled item IS Presented item (same object/features).
    # If they are same, distance is 0.
    
    # _get_weight_best calculates:
    # cdx = argmin(matchmat[i, :]) -> index of closest presented item to recalled item i.
    # If exact match exists (dist 0), it picks that.
    
    egg = quail.Egg(pres=pres, rec=rec, features=pres_feat)
    
    print(f"\nDEBUG: egg.pres shape: {egg.pres.shape}")
    print(f"DEBUG: egg.rec shape: {egg.rec.shape}")
    print(f"DEBUG: egg.pres content:\n{egg.pres}")
    print(f"DEBUG: egg.rec content:\n{egg.rec}")
    
    # Use match='best'
    res = fingerprint_helper(egg, match='best', features=['color'])
    assert res is not None
    assert not np.isnan(res)

    # Test with custom distance function?
    # Default color uses euclidean.
