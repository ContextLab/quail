# -*- coding: utf-8 -*-

from quail.analysis.analysis import analyze
from quail.egg import Egg, FriedEgg
from quail.load import load_example_data
import pytest
import pandas as pd
import six

# generate some fake data
presented = ['CAT', 'DOG', 'SHOE', 'HORSE']
recalled = ['HORSE', 'DOG', 'CAT']

features = [{
                    'category' : 'animal',
                    'size' : 'bigger',
                    'starting letter' : 'C',
                    'length' : 3
                 },
                 {
                    'category' : 'animal',
                    'size' : 'bigger',
                    'starting letter' : 'D',
                    'length' : 3
                 },
                 {
                    'category' : 'object',
                    'size' : 'smaller',
                    'starting letter' : 'S',
                    'length' : 4
                 },
                 {
                    'category' : 'animal',
                    'size' : 'bigger',
                    'starting letter' : 'H',
                    'length' : 5
                 }
]

egg = Egg(pres=[presented], rec=[recalled], features=[features])

def test_egg_works():
    assert isinstance(egg, Egg)

def test_pres_is_df():
    assert isinstance(egg.pres, pd.DataFrame)

def test_rec_is_df():
    assert isinstance(egg.rec, pd.DataFrame)

def test_pres_cells_are_dicts():
    assert isinstance(egg.pres.loc[0][0][0], dict)

def test_pres_cells_has_item():
    assert egg.pres.loc[0][0][0]['item']=='CAT'

def test_pres_cells_has_item():
    assert egg.rec.loc[0][0][0]['item']=='HORSE'

def test_distfuncs_is_dict():
    assert isinstance(egg.dist_funcs, dict)

def test_distfuncs_vals():
    assert all([val in ['euclidean', 'match'] for val in egg.dist_funcs.values()])

def test_egg_meta():
    assert isinstance(egg.meta, dict)

def test_egg_get_pres_items():
    assert isinstance(egg.get_pres_items(), pd.DataFrame)

def test_egg_get_pres_items_cat():
    assert egg.get_pres_items()[0][0][0]=='CAT'

def test_egg_get_pres_features():
    assert isinstance(egg.get_pres_features(), pd.DataFrame)

def test_egg_get_rec_items():
    assert isinstance(egg.get_rec_items(), pd.DataFrame)

def test_egg_get_rec_items_cat():
    assert egg.get_rec_items()[0][0][0]=='HORSE'

def test_egg_get_rec_features():
    assert isinstance(egg.get_rec_features(), pd.DataFrame)

def test_egg_crack():
    assert isinstance(egg.crack(), Egg)

def test_egg_crack_n_lists():
    assert egg.crack(lists=[0]).n_lists==1

def test_egg_crack_subjects():
    assert egg.crack(lists=[0], subjects=[0]).n_lists==1

def test_egg_to_dict():
    assert isinstance(egg.to_dict(), dict)

def test_egg_analyze():
    assert isinstance(egg.analyze('accuracy'), FriedEgg)

def test_egg_analyze_error():
    with pytest.raises(ValueError):
        egg.analyze('acc')

def test_egg_recmat():
    recmat = [[[3, 4, 2, 1, 0], [4, 2, 5, 3, 2]]]
    egg = Egg(recmat=recmat, list_length=10)
    assert isinstance(egg, Egg)


# Test DataFrame input support
class TestEggDataFrameInput:
    """Tests for creating Eggs from DataFrames directly."""

    def test_egg_from_dataframe(self):
        """Test that Egg can be created from DataFrames."""
        # Create test data as DataFrames
        pres_data = [[{'item': 'CAT', 'category': 'animal'},
                      {'item': 'DOG', 'category': 'animal'}],
                     [{'item': 'HAT', 'category': 'object'},
                      {'item': 'BAT', 'category': 'animal'}]]
        rec_data = [[{'item': 'DOG', 'category': 'animal'},
                     {'item': 'CAT', 'category': 'animal'}],
                    [{'item': 'BAT', 'category': 'animal'}]]

        # Create MultiIndex DataFrames
        index = pd.MultiIndex.from_tuples([(0, 0), (0, 1)], names=['subject', 'list'])
        pres_df = pd.DataFrame(pres_data, index=index)
        rec_df = pd.DataFrame(rec_data, index=index)

        egg_df = Egg(pres=pres_df, rec=rec_df)
        assert isinstance(egg_df, Egg)
        assert egg_df.n_subjects == 1
        assert egg_df.n_lists == 2
        assert egg_df.list_length == 2

    def test_egg_from_dataframe_dist_funcs(self):
        """Test that dist_funcs are properly inferred from DataFrame input."""
        pres_data = [[{'item': 'CAT', 'category': 'animal', 'temporal': 0},
                      {'item': 'DOG', 'category': 'animal', 'temporal': 1}]]
        rec_data = [[{'item': 'DOG', 'category': 'animal'}]]

        index = pd.MultiIndex.from_tuples([(0, 0)], names=['subject', 'list'])
        pres_df = pd.DataFrame(pres_data, index=index)
        rec_df = pd.DataFrame(rec_data, index=index)

        egg_df = Egg(pres=pres_df, rec=rec_df)
        assert 'category' in egg_df.dist_funcs
        assert 'temporal' in egg_df.dist_funcs
        assert egg_df.dist_funcs['category'] == 'match'
        assert egg_df.dist_funcs['temporal'] == 'euclidean'

    def test_egg_from_dataframe_custom_dist_funcs(self):
        """Test that custom dist_funcs override defaults for DataFrame input."""
        pres_data = [[{'item': 'CAT', 'size': 1.5}]]
        rec_data = [[{'item': 'CAT', 'size': 1.5}]]

        index = pd.MultiIndex.from_tuples([(0, 0)], names=['subject', 'list'])
        pres_df = pd.DataFrame(pres_data, index=index)
        rec_df = pd.DataFrame(rec_data, index=index)

        custom_dist = {'size': 'correlation'}
        egg_df = Egg(pres=pres_df, rec=rec_df, dist_funcs=custom_dist)
        assert egg_df.dist_funcs['size'] == 'correlation'

    def test_egg_from_dataframe_requires_multiindex(self):
        """Test that non-MultiIndex DataFrames raise ValueError."""
        pres_df = pd.DataFrame([[{'item': 'CAT'}]])
        rec_df = pd.DataFrame([[{'item': 'CAT'}]])

        with pytest.raises(ValueError, match="MultiIndex"):
            Egg(pres=pres_df, rec=rec_df)

    def test_egg_from_dataframe_analyze(self):
        """Test that egg created from DataFrame can be analyzed."""
        pres_data = [[{'item': 'CAT', 'category': 'animal', 'temporal': 0},
                      {'item': 'DOG', 'category': 'animal', 'temporal': 1},
                      {'item': 'HAT', 'category': 'object', 'temporal': 2},
                      {'item': 'BAT', 'category': 'animal', 'temporal': 3}]]
        rec_data = [[{'item': 'DOG', 'category': 'animal'},
                     {'item': 'CAT', 'category': 'animal'},
                     {'item': 'BAT', 'category': 'animal'}]]

        index = pd.MultiIndex.from_tuples([(0, 0)], names=['subject', 'list'])
        pres_df = pd.DataFrame(pres_data, index=index)
        rec_df = pd.DataFrame(rec_data, index=index)

        egg_df = Egg(pres=pres_df, rec=rec_df)
        result = egg_df.analyze('accuracy')
        assert isinstance(result, FriedEgg)

    def test_egg_from_dataframe_multiple_subjects(self):
        """Test DataFrame input with multiple subjects."""
        pres_data = [[{'item': 'CAT', 'temporal': 0}, {'item': 'DOG', 'temporal': 1}],
                     [{'item': 'HAT', 'temporal': 0}, {'item': 'BAT', 'temporal': 1}],
                     [{'item': 'RAT', 'temporal': 0}, {'item': 'MAT', 'temporal': 1}],
                     [{'item': 'SAT', 'temporal': 0}, {'item': 'PAT', 'temporal': 1}]]
        rec_data = [[{'item': 'DOG'}], [{'item': 'BAT'}],
                    [{'item': 'MAT'}], [{'item': 'PAT'}]]

        index = pd.MultiIndex.from_tuples([(0, 0), (0, 1), (1, 0), (1, 1)],
                                          names=['subject', 'list'])
        pres_df = pd.DataFrame(pres_data, index=index)
        rec_df = pd.DataFrame(rec_data, index=index)

        egg_df = Egg(pres=pres_df, rec=rec_df)
        assert egg_df.n_subjects == 2
        assert egg_df.n_lists == 2
