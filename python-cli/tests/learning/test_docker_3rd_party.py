import docker
import pytest
import os
import time

"""
Learning tests for the `docker` python package
"""

TEST_CONTAINER_NAME = "TestContainer"

def try_docker_cmd_optimistically(docker_cmd_that_might_fail, *args, **kwargs):
    try:
        docker_cmd_that_might_fail(*args, **kwargs)
    except docker.errors.APIError:
        # Ignore
        pass

class TestDockerModuleLearningTests:

    @pytest.fixture
    def client(self):
        client = docker.from_env()

        def cleanup_test_container():
            try:
                test_container = client.containers.get(TEST_CONTAINER_NAME)
                try_docker_cmd_optimistically(test_container.kill)
                try_docker_cmd_optimistically(test_container.remove, force=True)
            except docker.errors.NotFound:
                pass

        # Cleanup before test
        cleanup_test_container()

        # Yield client for tests
        yield client

        # Cleanup after test
        cleanup_test_container()



    @pytest.fixture
    def tmpdir_with_2_files(self, tmpdir):
        docker.from_env().containers.run
        hello = tmpdir.join('hello.txt')
        hello.write('Bonjour')
        goodbye = tmpdir.join('goodbye.txt')
        goodbye.write('Bonjour')
        return tmpdir

    class TestRun:
        def test_run_hello_world(self, client):
            cmd = "echo Hello World"
            res = client.containers.run("ubuntu:latest", cmd)
            assert res.decode('utf-8') == 'Hello World\n'

        def test_remove_disabled(self, client):
            # Given: Container started and immediately stopped by name, w/o remove option
            # Not detached & 'echo' cmd ==> Exits immediatley after 'echo'
            client.containers.run(
                "ubuntu:latest",
                "echo Hello World",
                name=TEST_CONTAINER_NAME)

            # When: Listing all containers
            all_containers = client.containers.list(all=True)
            all_containers_names = [
                c.name for c in all_containers]

            # Then: List contains test container
            assert TEST_CONTAINER_NAME in all_containers_names

        def test_remove_enabled(self, client):
            # Given: Container started and immediately stopped by name, WITH remove option
            # Not detached & 'echo' cmd ==> Exits immediatley after 'echo'
            client.containers.run(
                "ubuntu:latest",
                "echo Hello World",
                name=TEST_CONTAINER_NAME,
                remove=True)

            # When: Listing all containers
            all_containers_names = [c.name
                                    for c in client.containers.list(all=True)]

            # Then: List does not contain test container
            assert TEST_CONTAINER_NAME not in all_containers_names

        def test_mount_volumes(self, client, tmpdir_with_2_files):
            volume1_path = tmpdir_with_2_files
            volume1_mount_point = '/volumes_to_mount/vol1'

            res = client.containers.run(
                "ubuntu:latest",
                'ls /volumes_to_mount/vol1',
                volumes={
                    volume1_path: {
                        'bind': volume1_mount_point,
                        'mode': 'rw'
                    }
                })

            assert res.decode('utf-8') == 'goodbye.txt\nhello.txt\n'


    class TestRunBackground:
        def test_run_background(self, client):
            # Given: Container is started in the background
            client.containers.run(
                "ubuntu:latest",
                "tail -f /dev/null",
                name=TEST_CONTAINER_NAME,
                detach=True,
                remove=True)

            # When: Fetching its status
            container = client.containers.get(TEST_CONTAINER_NAME)
            status = container.status

            # Then: Container is running
            assert status == 'running'

        def test_kill_background(self, client): #TODO
            # Given: Container is started in the background
            client.containers.run(
                "ubuntu:latest",
                "tail -f /dev/null",
                name=TEST_CONTAINER_NAME,
                detach=True,
                remove=True)

            # When: Killing it and waiting 5s
            container = client.containers.get(TEST_CONTAINER_NAME)
            container.kill()
            time.sleep(5)

            # Then: Container is now killed
            with pytest.raises(docker.errors.NotFound):
                c = client.containers.get(TEST_CONTAINER_NAME)

        @pytest.mark.skip
        def test_check_is_running_background(self, client): #TODO
            raise NotImplementedError("TODO")

        @pytest.mark.skip
        def test_stop_background(self, client): #TODO
            raise NotImplementedError("TODO")

