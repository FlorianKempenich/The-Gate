"""
Adapter for the `docker` module
"""

import docker


class DockerApi():
    def __init__(self):
        self.docker = docker.from_env()

    def run(self, image_name, command, volumes=()):
        """ Run a container syncronously """
        volumes_dict = self.map_volumes(volumes)
        if not volumes_dict == {}:
            self.docker.containers.run(image_name, command, volumes=volumes_dict)
        else:
            self.docker.containers.run(image_name, command)

    def run_background(self, container_name, image_name, command, volumes=()):
        """ 
        Run a container asynchronously with the given name

        Returns:
            The container name formatted to be valid.

            Use this formatted name to operate on it in
            `is_running_background` and `stop_background`
        """
        formatted_name = self.format_name(container_name)
        return formatted_name

    def is_running_background(self, container_name):
        """ Check if a container is running in the background """
        raise NotImplementedError()

    def stop_background(self, container_name, image_name):
        """ Stop a container running in the background """
        raise NotImplementedError()


    @staticmethod
    def map_volumes(volumes_tuple: tuple):
        vol_dict = {}
        for vol in volumes_tuple:
            vol_params = vol.split(':')

            vol_path = vol_params[0]
            vol_mount_pt = vol_params[1]
            if len(vol_params) > 2:
                vol_mode = vol_params[2]
            else:
                vol_mode = 'rw'

            vol_dict[vol_path] = {
                'bind': vol_mount_pt,
                'mode': vol_mode
            }

        return vol_dict

    @staticmethod
    def format_name(container_name: str):
        return container_name\
                .strip()\
                .replace(' ', '-')

