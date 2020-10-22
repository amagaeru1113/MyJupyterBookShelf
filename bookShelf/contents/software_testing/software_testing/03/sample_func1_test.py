
import random

from sample_func1 import func1

def test_func1_n3():
    assert '3' == func1(3)

def test_func1_n5():
    assert '5' == func1(5)
    
def test_func1_na():
    l = list(range(100))
    l.remove(3)
    l.remove(5)
    
    num = random.choice(l)
    assert 'none' == func1(num)
