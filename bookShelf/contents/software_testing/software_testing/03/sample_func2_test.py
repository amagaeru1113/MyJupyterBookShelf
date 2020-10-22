
import random

from sample_func2 import func2

def test_func2_1():
    assert '2 ika' == func2(1)

def test_func2_2():
    assert '2 ika' == func2(2)
    
def test_func2_3():
    assert 'none' == func2(3)
    
def test_func2_6():
    assert 'none' == func2(6)
    
def test_func2_7():
    assert '7 ijo' == func2(7)
    
def test_func2_8():
    assert '7 ijo' == func2(8)
