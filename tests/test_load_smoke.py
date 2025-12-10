import pytest
import quail
import os
import joblib

def test_save_load_egg(tmp_path):
    # Setup Egg
    pres = [[['word1', 'word2']]]
    rec = [[['word2', 'word1']]]
    egg = quail.Egg(pres=pres, rec=rec)
    
    # Save path
    fname = tmp_path / "test_egg.egg"
    
    # Save
    egg.save(str(fname))
    
    # Check file exists
    assert os.path.exists(str(fname))
    
    # Load
    loaded_egg = quail.load_egg(str(fname))
    
    # Verify content
    assert loaded_egg.n_subjects == 1
    assert loaded_egg.get_pres_items().iloc[0].tolist() == ['word1', 'word2']

def test_save_load_fried_egg(tmp_path):
    # Create FriedEgg
    pres = [[['word1', 'word2']]]
    rec = [[['word2', 'word1']]]
    egg = quail.Egg(pres=pres, rec=rec)
    res = egg.analyze('accuracy')
    
    # Save
    fname = tmp_path / "test_res.fegg"
    res.save(str(fname))
    
    # Check
    assert os.path.exists(str(fname))
    
    # Load (requires updated load function? quail.load handles eggs, but what about fried eggs?)
    # quail.load helper or specific function?
    # quail/load.py has load_egg
    # But usually just quail.load() auto-detects?
    
    # Checking load.py source: load(path) calls joblib.load
    loaded_res = quail.load(str(fname))
    
    assert isinstance(loaded_res, quail.FriedEgg)
    # Check data
    assert loaded_res.data.equals(res.data)

def test_load_example_data():
    # Test loading built-in example
    try:
        egg = quail.load_example_data()
        assert isinstance(egg, quail.Egg)
        assert egg.n_subjects > 0
    except Exception as e:
        # Might fail if data file not found nearby or permission issue
        pytest.fail(f"Failed to load example data: {e}")
