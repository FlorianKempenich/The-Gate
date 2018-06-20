from mock import patch, MagicMock, call
import pytest
import tests.showcase.fake_lib

class TestDebugClasses:
    @patch('tests.showcase.fake_lib.get_instance')
    def test_nested_patching(self, get_instance_mock):
        get_instance_mock.return_value\
                .nested\
                .explode_nested.return_value = 'bonjour'

        fake_result = tests.showcase.fake_lib.get_instance().nested.explode_nested('hello')
        assert fake_result == 'bonjour'

