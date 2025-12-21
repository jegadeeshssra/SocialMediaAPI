import pytest   
from ..utils.calc import add

@pytest.mark.parametrize("num1 , num2 , expected" , [
    (1 , 2 , 3),
    (2 , 2 , 4),
    (3 , 2 , 5),
])
def test_add(num1 , num2 , expected):
    assert add(num1 , num2) == expected
