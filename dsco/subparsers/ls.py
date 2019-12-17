from pathlib import Path

# import os
# import yaml

import subprocess
from collections import OrderedDict
import json

# from dsco.helpers import docker_ps


# ======================================================================================
# Add subparser
#
cmd_name = Path(__file__).stem


def add_cmd(subparsers):
    cmd = subparsers.add_parser(cmd_name, help="list containers")
    cmd.add_argument(
        "-r",
        "--remote",
        action="store_true",
        help="list remote containers using docker-machine",
    )


def run_cmd(args, conf):
    # docker_ps(remote=args.remote)
    main(localhost=True, remote=args.remote)


def add_dispatch(dispatcher):
    dispatcher[cmd_name] = run_cmd


# ======================================================================================
# use docker to list images and containers
#
class Colors(object):
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKGREEN = "\033[92m"
    WARNING = "\033[92m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"

    @classmethod
    def container(cls, print_string):
        return cls.OKBLUE + print_string + cls.ENDC

    @classmethod
    def host(cls, print_string):
        return cls.BOLD + print_string + cls.ENDC


class Format(object):
    _join_char = ":&:"

    @classmethod
    def join_format_list(cls, format_list):
        return cls._join_char.join(i.format_string for i in format_list)

    @classmethod
    def format_output_to_dict(cls, format_list, format_output):
        value_list = format_output.split(cls._join_char)
        return {fmt.name: value for fmt, value in zip(format_list, value_list)}

    def __init__(self, name, format_string):
        self.name = name
        self.format_string = format_string

    def __str__(self):
        return self.format_string

    def __repr__(self):
        return f"{self.name}: {self.format_string}"


class Docker(object):
    """Encapsulate all the interactions with docker
    """

    # ==================================================================================
    # helpers
    #
    @classmethod
    def run_docker_cmd(cls, cmd, env=None):
        return subprocess.run(cmd, shell=True, capture_output=True, env=env, timeout=10)

    # ==================================================================================
    # docker-machine ls
    #
    machine_ls_docker_cmd = "docker-machine ls --format {{.Name}}"

    @classmethod
    def ls_machines(cls):
        """Get a list of docker machines

        Returns:
            list: machine names
        """
        machine_list = (
            Docker.run_docker_cmd(cls.machine_ls_docker_cmd)
            .stdout.decode("utf-8")
            .strip()
            .split("\n")
        )
        # output is a list of machine names
        return machine_list

    # ==================================================================================
    # docker images --format :
    #
    image_format_list = [
        Format(name="image", format_string="{{.Repository}}"),
        Format(name="tag", format_string="{{.Tag}}"),
        Format(name="id", format_string="{{.ID}}"),
        Format(name="created", format_string="{{.CreatedSince}}"),
        Format(name="size", format_string="{{.Size}}"),
    ]
    image_format_string = Format.join_format_list(image_format_list)
    images_docker_cmd = f"docker images --format '{image_format_string}'"

    @classmethod
    def images(cls, host):
        """Get a list of image properties on the specified host

        Args:
            host(Host): A host with a variable "docker_machine_env"
                The docker_machine_env is a dictionary of environment variables
                that will run docker commands on a remote docker machine.
                equivalent to docker-machine env {machine_name}

        Returns:
            image_list (list[dict]): A list of dictionaries for each image
                on the host. The dictionary is keyed from the name property
                of the image_format_list.
        """
        # each line contains information about an image
        images_docker_cmd_output = (
            cls.run_docker_cmd(cmd=cls.images_docker_cmd, env=host.docker_machine_env)
            .stdout.decode("utf-8")
            .strip()
            .split("\n")
        )
        # convert each line to a dictionary keyed by image_format_list
        image_list = [
            Format.format_output_to_dict(cls.image_format_list, line)
            for line in images_docker_cmd_output
        ]
        return image_list

    # ==================================================================================
    # docker ps --all --format :
    #
    ps_format_list = [
        Format(name="image", format_string="{{.Image}}"),
        Format(name="id", format_string="{{.ID}}"),
        Format(name="name", format_string="{{.Names}}"),
        Format(name="status", format_string="{{.Status}}"),
        Format(name="created", format_string="{{.CreatedAt}}"),
        Format(name="size", format_string="{{.Size}}"),
        Format(name="ports", format_string="{{.Ports}}"),
    ]
    ps_format_string = Format.join_format_list(ps_format_list)
    ps_docker_cmd = f"docker ps --all --format '{ps_format_string}'"

    @classmethod
    def ps(cls, host):
        """Get a list of container properties on the specified host

        Args:
            host(Host): A host with a variable "docker_machine_env"
                The docker_machine_env is a dictionary of environment variables
                that will run docker commands on a remote docker machine.
                equivalent to docker-machine env {machine_name}

        Returns:
            container_list (list[dict]): A list of dictionaries for each container
                on the host. The dictionary is keyed from the name property
                of the ps_format_list.
        """
        # each line contains information about a container
        ps_docker_cmd_output = (
            cls.run_docker_cmd(cmd=cls.ps_docker_cmd, env=host.docker_machine_env)
            .stdout.decode("utf-8")
            .strip()
            .split("\n")
        )
        # convert each line to a dictionary keyed by ps_format_list
        container_list = [
            Format.format_output_to_dict(cls.ps_format_list, line)
            for line in ps_docker_cmd_output
        ]
        return container_list

    # ==================================================================================
    # docker-machine inspect {machine_name}
    #
    inspect_machine_format_list = [
        # Format(name=__________ , format_string=__________)
        Format("tls_verify", "{{.HostOptions.EngineOptions.TlsVerify}}"),
        Format("ip", "{{.Driver.IPAddress}}"),
        Format("port", "{{.Driver.EnginePort}}"),
        Format("cert_path", "{{.HostOptions.AuthOptions.StorePath}}"),
        Format("machine_name", "{{.Name}}"),
    ]
    inspect_machine_format_string = Format.join_format_list(inspect_machine_format_list)
    inspect_machine_docker_cmd = (
        f"docker-machine inspect --format '{inspect_machine_format_string}'"
    )

    @classmethod
    def inspect_machine(cls, host):
        """Get properties of a docker-machine

        These properties can be used to create the environment variables 
        required to run docker commands on the docker-machine.

        Args:
            host(Host): Host needs a property "name" that corresponds
                to the name of the docker-machine.

        Returns:
            machine_info(dict): A dictionary of machine properties keyed
                by the name property of the inspect_machine_format_list.
        """
        cmd = f"{cls.inspect_machine_docker_cmd} {host.name}"
        inspect_machine_docker_cmd_output = (
            cls.run_docker_cmd(cmd).stdout.decode("utf-8").strip()
        )
        machine_info = Format.format_output_to_dict(
            cls.inspect_machine_format_list, inspect_machine_docker_cmd_output
        )
        return machine_info

    # ==================================================================================
    # docker inspect {container_name}
    #
    @classmethod
    def inspect_container(cls, host, container):
        """Get detailed information about a container

        This information is used to augment the information from the ps command.

        Args:
            host(Host): Host needs a property "docker_machine_env" to allow
                docker commands to be run against a specified docker-machine
            container (Container): Container needs a property "name" that
                corresponds to the name of the container and can be used 
                in the docker inspect command.

        Returns:
            docker_inspect_dict(dict): A dictionary of of container properties.
        """
        cmd = f"docker inspect {container.name}"
        docker_inspect_output = cls.run_docker_cmd(
            cmd, env=host.docker_machine_env
        ).stdout.decode("utf-8")
        docker_inspect_dict = json.loads(docker_inspect_output)[0]
        return docker_inspect_dict


class Container(object):
    """Contains functionality and properties of docker containers

    Args: 
        properties (dict): Properties derived from a docker ps cmd
        host (Host): A reference to the host the image is running on.

    Attributes:
        name (str): Container name
        image (str): Image the container was created from.
        properties:
            image (str): Image ID.
            name (str): Container name.
            status (str): Container status.
            created (str): Time when the container was created.
            port (str): Exposed ports.
        link (str): link to web server of container.

    """

    def __init__(self, properties, host):
        self.name = properties["name"]
        self.image = properties["image"]
        self.properties = properties
        self.host = host
        self.link = self._get_link()

    def _get_link(self):
        inspect_dict = Docker.inspect_container(self.host, self)

        # Port
        try:
            port = inspect_dict["HostConfig"]["PortBindings"]["80/tcp"][0]["HostPort"]
        except KeyError:
            port = "____"

        try:
            container_is_running = inspect_dict["State"]["Status"] == "running"
        except KeyError:
            container_is_running = False

        # ip
        ip = self.host.properties["ip"]
        link_ip = ip if container_is_running else "_" * len(ip)

        # link
        link = f"http://{link_ip}:{port}"

        return link

    def __str__(self):
        padded_name = f"    {self.name}"
        cols = [
            "{padded_name:<{NAME}}",
            "{link:<{LINK}}",
            "{id:<{ID}}",
            "{status:<{STATUS}}",
            "{_:<{SIZE}}",
        ]
        container_string = Colors.container(
            "".join(cols).format(
                **self.properties,
                **Inventory.columns,
                padded_name=padded_name,
                _="",
                link=self.link,
            )
        )
        return container_string

    def __repr__(self):
        return "{self.name}"


class Image(object):
    """Contains functionality and properties of docker images

    Args: 
        properties (dict): Properties derived from a docker images cmd
        host (Host): A reference to the host the image is running on.

    Attributes:
        name (str): Container name
        properties:
            image (str): Image repository.
            tag (str): Image tag.
            id (str): Image ID
            created (str): Elapsed time since the image was created
            size (str): Image disk size
            name (str): Combination of image and tag, {image:tag}.
    """

    def __init__(self, image_properties):
        self.properties = self._get_properties(image_properties)
        self.name = self.properties["name"]

    def _get_properties(self, properties):
        name = "{image}:{tag}".format(**properties)
        properties["name"] = name
        return properties

    def __str__(self):
        cols = [
            "{name:<{NAME}}",
            "{_:<{LINK}}",
            "{id:<{ID}}",
            "{created:<{STATUS}}",
            "{size:<{SIZE}}",
        ]
        return "".join(cols).format(**self.properties, **Inventory.columns, _="")

    def __repr__(self):
        return f"{self.name}"


class Host(object):
    def __init__(self, name):
        self.name = name
        self.properties = self._get_properties()
        self.docker_machine_env = self._get_docker_machine_env()
        self.image_list = self._list_images()
        self.container_list = self._list_containers()
        self.host_inventory = self._merge_items()

    # ----------------------------------------------------------------------------------
    # Host properties
    #
    def _get_properties(self):
        if self.name == "localhost":
            return dict(ip="localhost")
        else:
            return Docker.inspect_machine(self)

    # ----------------------------------------------------------------------------------
    # Docker machine env
    #
    def _get_docker_machine_env(self):
        """Create the environment variables for docker-machine

        Create the environment variables needed to run docker commands
        on the specified docker-machine.
        """
        if self.name == "localhost":
            return {}
        else:
            # construct env options from machine properties
            ip = self.properties["ip"]
            port = self.properties["port"]
            return dict(
                DOCKER_TLS_VERIFY=self.properties["tls_verify"],
                DOCKER_HOST=f"tcp://{ip}:{port}",
                DOCKER_CERT_PATH=self.properties["cert_path"],
                DOCKER_MACHINE_NAME=self.properties["machine_name"],
            )

    # ----------------------------------------------------------------------------------
    # Images / Containers
    #
    def _list_images(self):
        image_list = [Image(properties) for properties in Docker.images(self)]
        return image_list

    def _list_containers(self):
        container_list = [Container(properties, self) for properties in Docker.ps(self)]
        return container_list

    # ----------------------------------------------------------------------------------
    # Inventory
    #
    def _merge_items(self):
        host_inventory = OrderedDict(
            (image.name, dict(image=image, container_list=[]))
            for image in self.image_list
        )
        for container in self.container_list:
            try:
                image_key = next(
                    image.name
                    for image in self.image_list
                    if container.image in image.name
                )
            except StopIteration as e:
                print("=" * 100)
                print(f"= Container image: {container.image}")
                print("= Not found in images:")
                for image in self.image_list:
                    print(f"=     {image.name}")
                print("=" * 100)
                raise e

            host_inventory[image_key]["container_list"].append(container)

        return host_inventory

    # ----------------------------------------------------------------------------------
    # String
    #
    def __str__(self):
        lines = []

        for image_key in self.host_inventory.keys():
            image = self.host_inventory[image_key]["image"]
            lines.append(str(image))
            container_list = self.host_inventory[image_key]["container_list"]
            for container in container_list:
                lines.append(str(container))

        return "\n".join(lines)


class Inventory(object):
    columns = OrderedDict(NAME=34, LINK=48, ID=17, STATUS=31, SIZE=10)
    header = "".join(["{:<{}}".format(k, v) for k, v in columns.items()])
    line_len = sum(columns.values())

    def __init__(self, localhost=True, remote=False):
        self.hosts = []
        if localhost:
            self.hosts.append(Host("localhost"))

        if remote:
            docker_machine_list = Docker.ls_machines()
            for docker_machine in docker_machine_list:
                self.hosts.append(Host(docker_machine))

    def __str__(self):
        lines = []
        for host in self.hosts:
            lines.append(Colors.host(f"{host.name:-<{self.line_len}}"))
            lines.append(self.header)
            lines.append(str(host))

        return "\n".join(lines)


def main(localhost=False, remote=True):
    inventory = Inventory(localhost, remote)
    print(inventory)


if __name__ == "__main__":
    main()
