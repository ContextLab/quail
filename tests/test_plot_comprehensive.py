import pytest
import quail
import matplotlib.pyplot as plt

# Fixture for egg
@pytest.fixture
def egg():
    # 2 subjects, 2 lists each
    pres = [[['cat', 'dog', 'bat', 'rat'], ['fish', 'bird', 'worm', 'bug']],
            [['table', 'chair', 'desk', 'lamp'], ['sofa', 'bed', 'rug', 'mat']]]
    rec = [[['cat', 'dog', 'bat', 'rat'], ['fish', 'bird', 'worm', 'bug']],
           [['table', 'chair', 'desk', 'lamp'], ['sofa', 'bed', 'rug', 'mat']]]
    # Needs features for fingerprint
    features = [{'item': w, 'size': len(w)} for w in ['cat', 'dog', 'bat', 'rat', 'fish', 'bird', 'worm', 'bug', 'table', 'chair', 'desk', 'lamp', 'sofa', 'bed', 'rug', 'mat']]
    # Assign features to all
    # Using 1 big feature dict for simplicity via egg logic? 
    # Or pass explicit features structure.
    # Pres features must match structure.
    pres_feat = [[ [ {'size': len(w)} for w in lst ] for lst in sub ] for sub in pres]
    
    return quail.Egg(pres=pres, rec=rec, features=pres_feat)

def test_plot_acc_styles(egg):
    res = egg.analyze('accuracy')
    # Test styles
    res.plot(plot_style='bar', show=False)
    res.plot(plot_style='violin', show=False)
    res.plot(plot_style='swarm', show=False)
    plt.close('all')

def test_plot_grouping(egg):
    res = egg.analyze('accuracy')
    # Test groupings
    res.plot(plot_type='subject', show=False)
    res.plot(plot_type='list', show=False)
    # res.plot(plot_type='split', show=False) # split expects both?
    plt.close('all')

def test_plot_fingerprint(egg):
    res = egg.analyze('fingerprint', features=['size'])
    res.plot(plot_type='subject', show=False)
    # default style
    res.plot(show=False)
    plt.close('all')

def test_plot_spc(egg):
    res = egg.analyze('spc')
    res.plot(plot_type='subject', show=False)
    res.plot(plot_type='list', show=False)
    plt.close('all')

def test_plot_pnr(egg):
    res = egg.analyze('pnr') # defaults position 1?
    res.plot(plot_type='subject', show=False)
    plt.close('all')

def test_plot_lagcrp(egg):
    res = egg.analyze('lagcrp')
    res.plot(plot_type='subject', show=False)
    res.plot(plot_type='list', show=False)
    plt.close('all')

def test_plot_filtering(egg):
    res = egg.analyze('accuracy')
    # subconds
    # subjgroup must be defined?
    # egg has 2 subjects. default subjgroup [0, 1] (ints)?
    # subjconds must match.
    res.plot(subjconds=[0], show=False)
    
    # listconds
    # listgroup?
    # default listgroup [0, 1] per subj?
    # flattened levels?
    # let's try
    res.plot(listconds=[0], show=False)
    plt.close('all')
