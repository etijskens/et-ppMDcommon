# -*- coding: utf-8 -*-

"""Tests for et_ppmdcommon package."""

import numpy as np
import et_ppmdcommon as md


def test_addNoise():
    """Test for et_ppmdcommon.addNoise()."""
    x = np.array([0.0])
    y = np.array([0.0])
    noise = 1.0
    md.addNoise(x,y,noise)
    assert np.all(0 < np.sqrt(x*x +y*y))
    assert np.all(np.sqrt(x*x +y*y) < noise)
    print(x)
    print(y)

sqrt3 = np.sqrt(3)

def test_generateAtoms():
    r0 = 1
    xll, yll = 0.0, 0.0
    w = r0
    h = sqrt3
    box = md.Box(xll, yll, xll+w, yll+h)
    x, y = md.generateAtoms(box, r=r0)
    assert len(x)==2
    x_expected = np.array([0.,0.5])
    y_expected = np.array([0.,0.5*sqrt3])
    assert np.all(x == x_expected)
    assert np.all(y == y_expected)

    box = md.Box(xll+.1, yll+.1, xll+w-.1, yll+h-.1)
    x, y = md.generateAtoms(box, r=r0)
    # print(x)
    # print(y)
    assert len(x)==1
    x_expected = np.array([0.5])
    y_expected = np.array([0.5*sqrt3])
    assert np.all(x == x_expected)
    assert np.all(y == y_expected)

    box = md.Box(xll+.1, yll+.1, xll+w+.1, yll+h+.1)
    x, y = md.generateAtoms(box, r=r0)
    # print(x)
    # print(y)
    assert len(x)==2
    x_expected = np.array([0.5,1.])
    y_expected = np.array([0.5*sqrt3, sqrt3])
    assert np.all(x == x_expected)
    assert np.all(y == y_expected)

    box = md.Box(xll, yll, xll + 2*w, yll + h)
    x, y = md.generateAtoms(box, r=r0)
    assert len(x)==4
    x_expected = np.array([0.,0.5,1.,1.5])
    y_expected = np.array([0.,0.5*sqrt3,0.,0.5*sqrt3])
    assert np.all(x == x_expected)
    assert np.all(y == y_expected)


def test_Box():
    box = md.Box(0,0,1,1)
    assert box.inside(0, 0)
    assert box.inside(0, 0.5)
    assert box.inside(0.5, 0)
    assert box.inside(0.5, 0.5)
    assert not box.inside(0, 1)
    assert not box.inside(1, 0)
    assert not box.inside(0.5, 1)
    assert not box.inside(1, 0.5)
    assert not box.inside(0, 1)
    assert not box.inside(1, 1)

# ==============================================================================
# The code below is for debugging a particular test in eclipse/pydev.
# (otherwise all tests are normally run with pytest)
# Make sure that you run this code with the project directory as CWD, and
# that the source directory is on the path
# ==============================================================================
if __name__ == "__main__":
    the_test_you_want_to_debug = test_addNoise

    print("__main__ running", the_test_you_want_to_debug)
    the_test_you_want_to_debug()
    print('-*# finished #*-')
    
# eof