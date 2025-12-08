import pytest
import quail
import matplotlib.pyplot as plt

def test_plot_smoke():
    # Setup Minimal Egg
    pres = [[['cat', 'dog', 'bat', 'hat']]]
    rec = [[['bat', 'cat', 'dog']]]
    egg = quail.Egg(pres=pres, rec=rec)
    
    # 1. Accuracy
    print("Testing Accuracy Plot...")
    res = egg.analyze('accuracy')
    ax = quail.plot(res, show=False)
    assert ax is not None
    plt.close()

    # 2. SPC
    print("Testing SPC Plot...")
    res = egg.analyze('spc')
    ax = quail.plot(res, show=False)
    assert ax is not None
    plt.close()

    # 3. PFR
    print("Testing PFR Plot...")
    res = egg.analyze('pfr')
    ax = quail.plot(res, show=False)
    assert ax is not None
    plt.close()

    # 4. Lag-CRP
    print("Testing Lag-CRP Plot...")
    res = egg.analyze('lagcrp')
    ax = quail.plot(res, show=False)
    assert ax is not None
    plt.close()
    
    # 5. Fingerprint (Requires features)
    # Add features
    features = [{'item': 'cat', 'size': 10}, {'item': 'dog', 'size': 20}, 
                {'item': 'bat', 'size': 5}, {'item': 'hat', 'size': 5}]
    pres_feat = [[features]]
    # Rec features will be auto-mapped or we should pass them?
    # Egg matches by 'item' if features dict has item.
    
    # Correct constructor for features: 
    # pres can be list of list of dicts.
    egg_feat = quail.Egg(pres=pres_feat, rec=rec)
    
    print("Testing Fingerprint Plot...")
    res = egg_feat.analyze('fingerprint')
    ax = quail.plot(res, show=False)
    assert ax is not None
    plt.close()

def test_plot_customization():
    pres = [[['cat', 'dog']]]
    rec = [[['dog', 'cat']]]
    egg = quail.Egg(pres=pres, rec=rec)
    res = egg.analyze('accuracy')
    
    # Test title, xlim, ylim
    ax = quail.plot(res, title="Custom Title", xlim=[0, 1], ylim=[0, 1], show=False)
    assert ax.get_title() == "Custom Title"
    plt.close()

def test_plot_grouping():
    # 2 subjects, 2 lists
    pres = [[['a', 'b'], ['c', 'd']], [['e', 'f'], ['g', 'h']]]
    rec = [[['b', 'a'], ['d', 'c']], [['f', 'e'], ['h', 'g']]]
    egg = quail.Egg(pres=pres, rec=rec)
    
    res = egg.analyze('accuracy')
    
    # Plot subject
    ax = quail.plot(res, plot_type='subject', show=False)
    assert ax is not None
    plt.close()
    
    # Plot split
    # Split requires grouping variables usually?
    # Default listgroup is list index, subjgroup is subj index.
    ax = quail.plot(res, plot_type='split', show=False)
    assert ax is not None
    plt.close()
