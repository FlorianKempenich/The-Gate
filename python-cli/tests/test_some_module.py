from mock import patch, MagicMock
import pytest
from thegate.some_module import SomeClass

def test_simple():
    some_class = SomeClass()
    assert some_class.plus_2(5) == 7