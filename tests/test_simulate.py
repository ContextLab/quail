import pytest
import quail.simulate as simulate
import pandas as pd

def test_simulate_list():
    df = simulate.simulate_list()
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 16
    assert 'COLOR' in df.columns
