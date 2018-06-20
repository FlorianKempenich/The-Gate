"""
Adapter for the `docker` module
"""

import docker


class DockerApi():
    def __init__(self):
        self.docker = docker.from_env()

    def run(self, image_name, command, volumes=()):
        volumes_dict = self.map_volumes(volumes)
        if not volumes_dict == {}:
            docker.from_env().containers.run(image_name, command, volumes=volumes_dict)
        else:
            docker.from_env().containers.run(image_name, command)



    def run_background(self, container_name, image_name, command, volumes=()):
        raise NotImplementedError()

    def stop_background(self, container_name, image_name):
        raise NotImplementedError()

    @staticmethod
    def map_volumes(volumes_tuple: tuple):
        vol_dict = {}
        for vol in volumes_tuple:
            vol_params = vol.split(':')

            vol_path = vol_params[0]
            vol_mount_pt = vol_params[1]
            vol_mode = vol_params[2]

            vol_dict[vol_path] = {
                'bind': vol_mount_pt,
                'mode': vol_mode
            }

        return vol_dict
