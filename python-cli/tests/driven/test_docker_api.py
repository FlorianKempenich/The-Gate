"""
Test for the docker_api module
"""
import pytest
from mock import patch, MagicMock
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

#     @patch('docker.from_env')
#     def test_run_with_volume_multiple(self, from_env_mock, docker_api):
#         # Given: 'run' method is mocked
#         run_mock = MagicMock(name='containers.run')
#         from_env_mock.return_value\
#                 .containers\
#                 .run = run_mock
#
#         # When: Calling 'run'
#         docker_api.run("ubuntu:latest", "ls", ("/home:/mounted_home", "./other:/hey"))
#
#         # Then: Call has been relayed to 'docker' module
#         run_mock.assert_called_with("ubuntu:latest", "ls") #TODO
#
#     @patch('docker.from_env')
#     def test_run_with_volume_access_modifier(self, from_env_mock, docker_api):
#         # Given: 'run' method is mocked
#         run_mock = MagicMock(name='containers.run')
#         from_env_mock.return_value\
#                 .containers\
#                 .run = run_mock
#
#         # When: Calling 'run'
#         docker_api.run("ubuntu:latest", "ls", ("/home:/mounted_home:ro", "./other:/hey:rw"))
#
#         # Then: Call has been relayed to 'docker' module
#         run_mock.assert_called_with("ubuntu:latest", "ls") #TODO
#
#
#     @patch('docker.from_env')
#     def test_run_with_volume_access_modifier_default(self, from_env_mock, docker_api):
#         # Given: 'run' method is mocked
#         run_mock = MagicMock(name='containers.run')
#         from_env_mock.return_value\
#                 .containers\
#                 .run = run_mock
#
#         # When: Calling 'run'
#         docker_api.run("ubuntu:latest", "ls", ("/home:/mounted_home",))
#
#         # Then: Call has been relayed to 'docker' module
#         run_mock.assert_called_with("ubuntu:latest", "ls") #TODO
