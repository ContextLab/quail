# -*- coding: utf-8 -*-

import pytest
import quail
from quail.fingerprint import Fingerprint, OptimalPresenter
from quail.load import load_example_data

egg = load_example_data().crack(subjects=[0])
f = Fingerprint()
f_egg = Fingerprint(init=egg)
f_egg_perm = Fingerprint(init=egg, permute=True, nperms=10)

def test_fingerprint_init():
    assert isinstance(f, quail.Fingerprint)

def test_fingerprint_init_with_egg():
    assert isinstance(f, quail.Fingerprint)

def test_fingerprint_init_with_egg_permute():
    assert isinstance(f_egg_perm, quail.Fingerprint)

def test_fingerprint_update():
    f.update(egg)
    assert isinstance(f, quail.Fingerprint)
    assert len(f.history)==1

def test_fingerprint_get_features():
    assert isinstance(f_egg.get_features(), list)

presenter = OptimalPresenter()
params = {
    'fingerprint' : f
}
presenter_params = OptimalPresenter(params=params, strategy='stabilize')

def test_optimal_presenter_init():
    assert isinstance(presenter, quail.OptimalPresenter)

def test_optimal_presenter_init_w_params():
    assert isinstance(presenter_params, quail.OptimalPresenter)

def test_optimal_presenter_set_params():
    presenter_params.set_params('alpha', 3)
    assert presenter_params.get_params('alpha') is 3

def test_optimal_presenter_set_strategy():
    presenter_params.set_strategy('stabilize')
    assert presenter_params.strategy is 'stabilize'

def test_optimal_presenter_order():
    egg = load_example_data()
    egg_slice = egg.crack(subjects=[0], lists=[0])
    reordered_egg = presenter.order(egg_slice, nperms=10)
    assert isinstance(reordered_egg, quail.Egg)
