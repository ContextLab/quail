import pytest
import quail
import os
import joblib

def test_egg_info(capsys):
    pres = [[['a']]]
    rec = [[['a']]]
    egg = quail.Egg(pres=pres, rec=rec, meta={'foo': 'bar'})
    
    egg.info()
    captured = capsys.readouterr()
    assert 'Number of subjects: 1' in captured.out
    assert 'Meta data: {\'foo\': \'bar\'}' in captured.out

def test_egg_save_load(tmpdir):
    pres = [[['a']]]
    rec = [[['a']]]
    egg = quail.Egg(pres=pres, rec=rec)
    
    # Save
    path = str(tmpdir.join('test_egg.egg'))
    egg.save(path)
    
    assert os.path.exists(path)
    
    # Load (manual load since Egg doesn't have load classmethod, probably quail.load functions do)
    # But joblib.load should work to inspect it
    loaded_dict = joblib.load(path)
    assert isinstance(loaded_dict, dict)
    assert 'pres' in loaded_dict
    assert isinstance(loaded_dict['pres'], list)
    # Check item in first position
    assert loaded_dict['pres'][0][0][0]['item'] == 'a'

def test_fried_egg_save(tmpdir):
    fegg = quail.FriedEgg(data=[1, 2, 3], analysis='dummy')
    
    path = str(tmpdir.join('test_fegg')) # Extension should be added
    fegg.save(path)
    
    expected_path = path + '.fegg'
    assert os.path.exists(expected_path)
    
    loaded = joblib.load(expected_path)
    assert loaded['analysis'] == 'dummy'
    assert loaded['data'] == [1, 2, 3]

def test_egg_to_dict_json():
    pres = [[['a']]]
    rec = [[['a']]]
    egg = quail.Egg(pres=pres, rec=rec)
    
    d = egg.to_dict()
    assert isinstance(d, dict)
    assert 'pres' in d
    assert isinstance(d['pres'], list)
    
    j = egg.to_json()
    assert isinstance(j, dict)
    # checking json string format?
    # egg.to_json returns dict of JSON strings for DFs
    assert isinstance(j['pres'], str)
