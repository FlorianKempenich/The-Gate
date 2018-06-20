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
