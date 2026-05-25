# 1. FIX: Make sure all three functions are imported here!
from math_ops import add, is_positive, is_greater_than_ten

def test_add():
    assert add(2, 3) == 5

def test_is_positive():
    assert is_positive(5) == True
    assert is_positive(0) == False 

def test_is_greater_than_ten():
    # 2. WEAK TEST: This will pass even if the code mutates to >=
    assert is_greater_than_ten(15) == True