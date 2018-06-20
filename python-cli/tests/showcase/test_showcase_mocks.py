from mock import patch, MagicMock
import pytest

"""
This is a debug class. Only here to showcase how to implement tests with pytest.

Class hierarchy to patch
"""


class MotherClass():
    def __init__(self):
        print('I am the mother class')

    def exploding_method(self, text=''):
        raise Exception(''.join(["Exploding method!!", text]))


class ChildClass(MotherClass):
    # def __init__(self):
    #     print('I am child class')
    def call_the_exploding_of_mother(self):
        return self.exploding_method()

    def call_the_exploding_of_mother_with_args(self):
        return self.exploding_method(text='hellooooo')


class UnrelatedClass():
    def __init__(self):
        print('I am unrelated')

    def call_the_exploding_of_mother_via_child(self):
        child = ChildClass()
        child.call_the_exploding_of_mother()

class ComplexClass():
    @property
    def nested(self):
        return NestedClass()

class NestedClass():
    def explode_nested(self):
        raise Exception('I am the nested class')
###################################################


@pytest.mark.skip
class TestDebugClasses:
    def test_without_mocking(self):
        child = ChildClass()
        with pytest.raises(Exception, message='Exploding method!!'):
            child.call_the_exploding_of_mother()


    def test_without_mocking_2(self):
        child = ChildClass()
        with pytest.raises(Exception, message='Exploding method!!hellooooo'):
            child.call_the_exploding_of_mother_with_args()


    @patch('tests.test_showcase_mocks.MotherClass.exploding_method')
    def test_mocking_exploding(self, exploding_method):
        exploding_method.return_value = 'moooooooocked'
        child = ChildClass()
        assert child.call_the_exploding_of_mother() == 'moooooooocked'


    @patch.object(MotherClass, 'exploding_method')
    def test_mocking_exploding_via_object(self, exploding_method):
        exploding_method.return_value = 'moooooooocked'
        child = ChildClass()
        assert child.call_the_exploding_of_mother() == 'moooooooocked'


    @patch.object(MotherClass, 'exploding_method')
    def test_mocking_exploding_via_object_2(self, exploding_method):
        exploding_method.return_value = 'moooooooocked'
        child = ChildClass()
        a = MagicMock()
        a.call_args
        a.call_args_list
        child.call_the_exploding_of_mother_with_args()
        exploding_method.assert_called_once()
        print(exploding_method.call_args)
        print(exploding_method.call_args_list)
        # assert 1 == 3
        # assert child.call_the_exploding_of_mother() == 'moooooooocked'

    #@patch.object(ComplexClass, 'nested.explode_nested')
    @patch.object(ComplexClass, 'nested')
    def test_with_nested_class(self, nested_property: MagicMock):
        with_nested = ComplexClass()
        with_nested.nested.explode_nested()
        print(nested_property.method_calls)
