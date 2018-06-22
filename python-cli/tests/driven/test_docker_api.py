"""
Test for the docker_api module

This test only tests the interactions with the `docker` module.
To ensure that the `docker` module actually does what it's supposed to, check the 
learning tests.
"""
import pytest
from mock import patch, MagicMock, call
from thegate.driven.docker_api import DockerApi


@pytest.fixture
def containers_run_mock():
    return MagicMock(name='containers.run')


@pytest.fixture
def docker_api(containers_run_mock):
    def patch_docker_module(containers_run_mock: MagicMock):
        patched_docker_module = patch('thegate.driven.docker_api.docker')

        docker_mock = patched_docker_module.start()
        docker_mock\
            .from_env.return_value\
            .containers\
            .run = containers_run_mock

        return patched_docker_module

    def unpatch_docker_module(patched_docker_module):
        patched_docker_module.stop()

    patched_docker_module = patch_docker_module(containers_run_mock)
    yield DockerApi()
    unpatch_docker_module(patched_docker_module)


class TestRun:
    def test_returns_none(self, docker_api, containers_run_mock):
        """
        Test docstring
        """
        res = docker_api.run("ubuntu:latest", "ls")
        assert res == None

    def test_simple_run(self, docker_api, containers_run_mock):
        docker_api.run("ubuntu:latest", "ls")
        containers_run_mock.assert_called_with("ubuntu:latest", "ls")

    def test_run_with_volume_single(self, docker_api, containers_run_mock):
        docker_api.run("ubuntu:latest", "ls",
                       volumes=("/home:/mounted_home:rw",))

        containers_run_mock.assert_called_with(
            "ubuntu:latest",
            "ls",
            volumes={
                '/home': {
                    'bind': '/mounted_home',
                    'mode': 'rw'
                }
            })

    def test_run_with_volume_single_default_mode(self, docker_api, containers_run_mock):
        docker_api.run("ubuntu:latest", "ls",
                       volumes=("/home:/mounted_home",))

        containers_run_mock.assert_called_with(
            "ubuntu:latest",
            "ls",
            volumes={
                '/home': {
                    'bind': '/mounted_home',
                    'mode': 'rw'  # Default is 'rw'
                }
            })

    def test_run_with_volume_multiple(self, docker_api, containers_run_mock):
        docker_api.run("ubuntu:latest", "ls",
                       volumes=("/home:/mounted_home:ro", "./other:/hey",))

        containers_run_mock.assert_called_with(
            "ubuntu:latest",
            "ls",
            volumes={
                '/home': {
                    'bind': '/mounted_home',
                    'mode': 'ro'
                },
                './other': {
                    'bind': '/hey',
                    'mode': 'rw'  # Default is 'rw'
                }
            })

class TestRunBackground:
    class TestFormatName:
        def test_valid(self, docker_api):
            res = docker_api.run_background("TestContainer", "ubuntu:latest", "tail -f /dev/null")
            assert res == "TestContainer"

        def test_leading_space(self, docker_api):
            res = docker_api.run_background("    TestContainer", "ubuntu:latest", "tail -f /dev/null")
            assert res == "TestContainer"

        def test_trailing_space(self, docker_api):
            res = docker_api.run_background("TestContainer    ", "ubuntu:latest", "tail -f /dev/null")
            assert res == "TestContainer"

        def test_replace_space_with_dash(self, docker_api):
            res = docker_api.run_background("Test Container", "ubuntu:latest", "tail -f /dev/null")
            assert res == "Test-Container"

        def test_replace_multiple_spaces_with_single_dash(self, docker_api):
            res = docker_api.run_background("Test       Container", "ubuntu:latest", "tail -f /dev/null")
            assert res == "Test-Container"

        def test_all_combined(self, docker_api):
            res = docker_api.run_background("  Test    Container  ", "ubuntu:latest", "tail -f /dev/null")
            assert res == "Test-Container"

    def test_simple_run(self, docker_api, containers_run_mock: MagicMock):
        docker_api.run_background("TestContainer", "ubuntu", "ls")

        run_called_with_args, run_called_with_kwargs = containers_run_mock.call_args

        # Assertions on call arguments have been decomposed to not have 
        # to tests wether more kwargs options are used.
        # In particular the `remove` option is tested in another test
        assert ("ubuntu", "ls") == run_called_with_args
        assert 'name' in run_called_with_kwargs
        assert run_called_with_kwargs['name'] == "TestContainer"
        assert 'detach' in run_called_with_kwargs
        assert run_called_with_kwargs['detach'] == True

