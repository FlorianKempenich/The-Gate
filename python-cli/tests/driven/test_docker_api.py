"""
Test for the docker_api module
"""
import pytest
from mock import patch, MagicMock
from thegate.driven.docker_api import DockerApi


@pytest.fixture
def docker_api():
    return DockerApi()


class TestRun:
    @patch('docker.from_env')
    def test_simple_run(self, from_env_mock, docker_api):
        # Given: 'run' method is mocked
        run_mock = MagicMock(name='containers.run')
        from_env_mock.return_value\
            .containers\
            .run = run_mock

        # When: Calling 'run'
        docker_api.run("ubuntu:latest", "ls")

        # Then: Call has been relayed to 'docker' module
        run_mock.assert_called_with("ubuntu:latest", "ls")

    @patch('docker.from_env')
    def test_run_with_volume_single(self, from_env_mock, docker_api):
        # Given: 'run' method is mocked
        run_mock = MagicMock(name='containers.run')
        from_env_mock.return_value\
            .containers\
            .run = run_mock

        # When: Calling 'run'
        docker_api.run("ubuntu:latest", "ls", volumes=("/home:/mounted_home:rw",))

        # Then: Call has been relayed to 'docker' module
        run_mock.assert_called_with(
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
