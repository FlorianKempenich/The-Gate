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
    """
    Mock for the call to 'docker.from_env().containers.run(.....)'
    Use for assertions.
    """
    return MagicMock(name='containers.run')


@pytest.fixture
def docker_module_mock(containers_run_mock):
    """
    Mock for the entire 'docker' module.

    Do not access directly for assertions.
    Use the `containers_run_mock` instead
    """
    class DockerModulePatcher:
        def patch(self):
            self.patched_docker_module = patch(
                'thegate.driven.docker_api.docker')
            self.docker_module_mock = self.patched_docker_module.start()

        def attach_containers_run_mock(self):
            self.docker_module_mock\
                .from_env.return_value\
                .containers\
                .run = containers_run_mock

        def unpatch(self):
            self.patched_docker_module.stop()

    docker_module_patcher = DockerModulePatcher()
    docker_module_patcher.patch()
    docker_module_patcher.attach_containers_run_mock()

    yield docker_module_patcher.docker_module_mock

    docker_module_patcher.unpatch()


@pytest.fixture
def docker_api(docker_module_mock):
    return DockerApi()


@pytest.fixture
def assert_docker_lib_called_with_args(containers_run_mock):
    def do_assert_with_given_args(*args):
        """ 
        Assert that the 'docker.from_env().containers.run(..)' method
        has been called with the given arguments.

        Does not check keyword arguments!

        """
        run_called_with_args, _ = containers_run_mock.call_args
        assert args == run_called_with_args

    return do_assert_with_given_args


@pytest.fixture
def assert_docker_lib_called_with_options(containers_run_mock):
    def do_assert_with_given_options(**expected_opts_as_kwargs):
        """ 
        Assert that the 'docker.from_env().containers.run(..)' method
        has been called with the given options (keyword arguments)

        It is not exclusive! Other options might have been given.

        Does not check regular arguments!
        """
        _, run_called_with_kwargs = containers_run_mock.call_args
        for option in expected_opts_as_kwargs:
            assert option in run_called_with_kwargs
            assert expected_opts_as_kwargs[option] == run_called_with_kwargs[option]

    return do_assert_with_given_options


class TestRun:
    def test_returns_none(self, docker_api, containers_run_mock):
        """
        Test docstring
        """
        res = docker_api.run("ubuntu:latest", "ls")
        assert res == None

    def test_simple_run(self, docker_api, assert_docker_lib_called_with_args):
        docker_api.run("ubuntu:latest", "ls")
        assert_docker_lib_called_with_args("ubuntu:latest", "ls")

    def test_run_with_volume_single(self, docker_api, assert_docker_lib_called_with_options):
        docker_api.run("ubuntu:latest", "ls",
                       volumes=("/home:/mounted_home:rw",))

        assert_docker_lib_called_with_options(volumes={
            '/home': {
                'bind': '/mounted_home',
                'mode': 'rw'
            }
        })

    def test_run_with_volume_single_default_mode(self, docker_api, assert_docker_lib_called_with_options):
        docker_api.run("ubuntu:latest", "ls",
                       volumes=("/home:/mounted_home",))

        assert_docker_lib_called_with_options(
            volumes={
                '/home': {
                    'bind': '/mounted_home',
                    'mode': 'rw'  # Default is 'rw'
                }
            })

    def test_run_with_volume_multiple(self, docker_api, assert_docker_lib_called_with_options):
        docker_api.run("ubuntu:latest", "ls",
                       volumes=("/home:/mounted_home:ro", "./other:/hey",))

        assert_docker_lib_called_with_options(volumes={
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
            res = docker_api.run_background(
                "TestContainer", "ubuntu:latest", "tail -f /dev/null")
            assert res == "TestContainer"

        def test_leading_space(self, docker_api):
            res = docker_api.run_background(
                "    TestContainer", "ubuntu:latest", "tail -f /dev/null")
            assert res == "TestContainer"

        def test_trailing_space(self, docker_api):
            res = docker_api.run_background(
                "TestContainer    ", "ubuntu:latest", "tail -f /dev/null")
            assert res == "TestContainer"

        def test_replace_space_with_dash(self, docker_api):
            res = docker_api.run_background(
                "Test Container", "ubuntu:latest", "tail -f /dev/null")
            assert res == "Test-Container"

        def test_replace_multiple_spaces_with_single_dash(self, docker_api):
            res = docker_api.run_background(
                "Test       Container", "ubuntu:latest", "tail -f /dev/null")
            assert res == "Test-Container"

        def test_all_combined(self, docker_api):
            res = docker_api.run_background(
                "  Test    Container  ", "ubuntu:latest", "tail -f /dev/null")
            assert res == "Test-Container"

    def test_simple_run(
            self,
            docker_api,
            assert_docker_lib_called_with_args,
            assert_docker_lib_called_with_options):
        docker_api.run_background("TestContainer", "ubuntu", "ls")

        assert_docker_lib_called_with_args("ubuntu", "ls")
        assert_docker_lib_called_with_options(detach=True)

    def test_container_started_with_rm_option(
            self,
            docker_api,
            assert_docker_lib_called_with_options):
        docker_api.run_background("TestContainer", "ubuntu", "ls")

        assert_docker_lib_called_with_options(remove=True)

    def test_container_started_with_formatted_name(
            self,
            docker_api,
            assert_docker_lib_called_with_options):
        docker_api.run_background("   Test    Container  ", "ubuntu", "ls")

        assert_docker_lib_called_with_options(name="Test-Container")

    def test_with_volumes(
            self,
            docker_api,
            assert_docker_lib_called_with_options):
        docker_api.run_background(
            "TestContainer",
            "ubuntu:latest",
            "ls",
            volumes=("/home:/mounted_home:ro", "./other:/hey",))

        assert_docker_lib_called_with_options(volumes={
            '/home': {
                'bind': '/mounted_home',
                'mode': 'ro'
            },
            './other': {
                'bind': '/hey',
                'mode': 'rw'  # Default is 'rw'
            }
        })


class TestIsRunningBackground:
    #  def stop_background(self, container_name, image_name):
    #      raise NotImplementedError()
    @pytest.mark.skip
    def test_is_running(self, docker_api):  # TODO

        docker_api.is_running_background("Test Container")

