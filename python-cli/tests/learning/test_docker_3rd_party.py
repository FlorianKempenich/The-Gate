import docker
import pytest
import os

"""
Learning tests for the `docker` python package
"""

@pytest.mark.skip(reason="Learning tests involving Docker -> Slow to run")
class TestDockerModuleLearningTests:

    @pytest.fixture
    def client(self):
        return docker.from_env()

    @pytest.fixture
    def tmpdir_with_2_files(self, tmpdir):
        hello = tmpdir.join('hello.txt')
        hello.write('Bonjour')
        goodbye = tmpdir.join('goodbye.txt')
        goodbye.write('Bonjour')
        return tmpdir

    def test_run_hello_world(self, client):
        cmd = "echo Hello World"
        res = client.containers.run("ubuntu:latest", cmd)
        assert res.decode('utf-8') == 'Hello World\n'

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

    def test_run_background(self, client):
        # Given: Container is started in the background
        container_name = "TestContainer"
        client.containers.run(
            "ubuntu:latest",
            "tail -f /dev/null",
            name=container_name,
            detach=True,
            remove=True)

        # When: Fetching its status, and then killing it
        container = client.containers.get(container_name)
        status_while_running = container.status
        container.kill()

        # Then: Container was running and now is killed
        assert status_while_running == 'running'
        with pytest.raises(docker.errors.NotFound):
            client.containers.get(container_name)

    def test_remove_disabled(self, client):
        # Given: Container started and immediately stopped by name, w/o remove option
        container_name = "TestContainer"
        # Not detached & 'echo' cmd ==> Exits immediatley after 'echo'
        client.containers.run(
            "ubuntu:latest",
            "echo Hello World",
            name=container_name)

        # When: Listing all containers, and then remove container
        all_containers_before_removal = client.containers.list(all=True)
        all_containers_names_before_removal = [
            c.name for c in all_containers_before_removal]

        client.containers.get(container_name).remove()

        # Then: List contains test container
        assert container_name in all_containers_names_before_removal

    def test_remove_enabled(self, client):
        # Given: Container started and immediately stopped by name, WITH remove option
        container_name = "TestContainer"
        # Not detached & 'echo' cmd ==> Exits immediatley after 'echo'
        client.containers.run(
            "ubuntu:latest",
            "echo Hello World",
            name=container_name,
            remove=True)

        # When: Listing all containers
        all_containers_names = [c.name
                                for c in client.containers.list(all=True)]

        # Then: List does not contain test container
        assert container_name not in all_containers_names
