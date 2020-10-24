
from exercises_1 import func_exe

def test_exercises_1():
    assert 300 == func_exe('セットA')

def test_exercises_2():
    assert 500 == func_exe('セットB')

def test_exercises_3():
    assert 800 == func_exe('セットC')
    
def test_exercises_4():
    assert 0 == func_exe('セットD')
