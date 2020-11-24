"""ls: information about images and containers

Use 'dsco ls' to get information about images and containers running 
on your localhost. Use 'dsco ls -r' to add information about machines 
listed in $HOME/.dsco/settings.json
"""
from pathlib import Path
import concurrent.futures

import os

# import yaml

import subprocess
from collections import OrderedDict
import json

from dsco.local_options import Settings


# ======================================================================================
# Add subparser
#
cmd_name = Path(__file__).stem


def add_subparser(subparsers):
    sub = subparsers.add_parser(cmd_name, help="list containers")
    sub.add_argument(
        "-r",
        "--remote",
        action="store_true",
        help="list remote containers using docker over ssh",
    )


def run_cmd(args, conf):
    main(localhost=True, remote=args.remote)


def add_dispatch(dispatcher):
    dispatcher[cmd_name] = run_cmd


# ======================================================================================
# use docker to list images and containers
#
class Colors(object):
    """Define colors and methods to apply formatting to strings

    Use the methods to apply formatting to the specified string type. 

    Methods
        container (str): Add container formatting to input string.
        host (str): Add host formatting to input string.
        header (str): Add header formatting to input string.

    Example
        header = Colors.header(header_string)
        print(header)
    """

    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKGREEN = "\033[92m"
    WARNING = "\033[92m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    REVERSED = "\u001b[7m"

    @classmethod
    def container(cls, print_string):
        return cls.OKBLUE + print_string + cls.ENDC

    @classmethod
    def host(cls, print_string):
        # return cls.BOLD + print_string + cls.ENDC
        return cls.REVERSED + print_string + cls.ENDC

    @classmethod
    def header(cls, print_string):
        return cls.UNDERLINE + print_string + cls.ENDC


class Format(object):
    """Facilitate building and parsing docker format strings

    The formatting option (--format) will pretty print some of the 
    docker commands output using a Go template.

    For example:

        docker images --format '{{.Repository}}:&:{{.Tag}}'
    
    will print images with the repository name and image tag seperated 
    by ':&:':

        "foo_dev:&:latest"

    There are many cases where we want to build these format strings 
    and then collect the output in a dictionary. To continue with the 
    example, we would like to process the output string into the 
    following dictionary:

        dict(name = foo_dev, tag=latest)

    This class facilitates the building of the format strings and the 
    parsing of corresponding docker output.

    Methods
        join_format_list (format_list): Given a list of Format objects 
            return a docker '--format' string.
        format_output_to_dict (format_list, format_output): Convert 
            output of a docker --format command to a dictionary.
    """

    _join_char = ":&:"

    @classmethod
    def join_format_list(cls, format_list):
        """Return a docker '--format' string from a list of Format objects.

        Args
            format_list (List[Format]): 
                A list of Format objects. Each 
                one corresponds to a different piece of information 
                about the docker object
        
        Returns
            A format string to be used with the --format options of a 
            docker command.

        Example
            The docker command to return 'Image Repository' and 
            'Image Tag' information is:
            
                docker images --format '{{.Repository}}:&:{{.Tag}}'
            
            To use this method to generate that string we would create 
            the list:

            .. code-block:: python

                format_list = [
                    Format(name="image", format_string="{{.Repository}}"),
                    Format(name="tag", format_string="{{.Tag}}")
                ]

            The method would then return:

                "'{{.Repository}}:&:{{.Tag}}'"
        """
        return cls._join_char.join(i.format_string for i in format_list)

    @classmethod
    def format_output_to_dict(cls, format_list, format_output):
        """ Convert output of a docker --format command to a dictionary

        Args
            format_list (List[Format]): 
                A list of Format objects. Each 
                one corresponds to a different piece of information 
                about the docker object
            format_output (str): 
                One line from the output of the 
                'docker --format' command.
        
        Returns
            A dictionary where :code:`keys = [key.name for key in format_list]`
            and values are equal to the corresponding fields from 
            the 'docker --format' command.

        Example
            Continuing from the example in :py:func:`join_format_list` we had:
                
            format_list:

            .. code-block:: python

                format_list = [
                    Format(name="image", format_string="{{.Repository}}"),
                    Format(name="tag", format_string="{{.Tag}}")
                ]

            docker command:

            .. code-block::

                    docker images --format '{{.Repository}}:&:{{.Tag}}'
            
            Sample output:
            
            .. code-block::

                    foo:&:latest
                    bar:&:4.8

            .. code-block::python

                format_output_to_dict(format_list, "foo:&:latest") 
                
            would return 
            
            .. code-block::

                dict(image="foo", tag="latest")
        """
        value_list = format_output.split(cls._join_char)
        return {fmt.name: value for fmt, value in zip(format_list, value_list)}

    def __init__(self, name, format_string):
        """
        Args
            name (str): A descriptive name of the format
            format_string (str): The docker format code.
        """
        self.name = name
        self.format_string = format_string

    def __str__(self):
        return self.format_string

    def __repr__(self):
        return f"{self.name}: {self.format_string}"


class Docker(object):
    """Encapsulate all the interactions with docker

    Attributes
        images_docker_cmd (str): The 'docker images' command run to get 
            information about the docker images.
        ps_docker_cmd (str): The 'docker ps' command run to get 
            information about the docker containers.

    Methods
        run_docker_cmd (cmd, env): Convenience function to run 
            docker commands.
        images (Host): Return information on all docker images on the 
            given host.
        ps (Container): Return information on all docker containers on 
            the given host.
        inspect_container (Container): Return detailed information on 
            the given container.
    """

    # ==================================================================================
    # helpers
    #
    @classmethod
    def run_docker_cmd(cls, cmd, env=None):
        """Convenience function to run docker commands
        
        Adds try/except, and the following options:
            - shell=True
            - capture_output=True
            - timeout=15

        Args
            cmd (str): 
                The docker command to be run.
            env (dict): 
                A dictionary containing all the necessary 
                environment variables to run the docker command.

        Returns
            completed_process (subprocess.CompletedProcess):
                Information about the output of the command.
        """
        try:
            completed_process = subprocess.run(
                cmd, shell=True, capture_output=True, env=env, timeout=15
            )
        except subprocess.TimeoutExpired:
            completed_process = None

        return completed_process

    # ==================================================================================
    # docker images --format :
    #
    _image_format_list = [
        Format(name="image", format_string="{{.Repository}}"),
        Format(name="tag", format_string="{{.Tag}}"),
        Format(name="id", format_string="{{.ID}}"),
        Format(name="created", format_string="{{.CreatedSince}}"),
        Format(name="size", format_string="{{.Size}}"),
    ]
    _image_format_string = Format.join_format_list(_image_format_list)
    images_docker_cmd = f"docker images --no-trunc --format '{_image_format_string}'"

    @classmethod
    def images(cls, host):
        """Get a list of image properties on the specified host

        Args:
            host(Host): A host object with the attribute "docker_env".

        Returns:
            image_list (list[dict]): A list containing a dictionary for 
                each image on the host. The dictionary is keyed from the 
                name property of the _image_format_list.
        """
        try:
            # each line contains information about an image
            images_docker_cmd_output = (
                cls.run_docker_cmd(cmd=cls.images_docker_cmd, env=host.docker_env)
                .stdout.decode("utf-8")
                .strip()
                .split("\n")
            )

            no_images = images_docker_cmd_output == [""]
            if no_images:
                raise ValueError

        except (AttributeError, ValueError):
            images_docker_cmd_output = []

        # convert each line to a dictionary keyed by _image_format_list
        image_list = [
            Format.format_output_to_dict(cls._image_format_list, line)
            for line in images_docker_cmd_output
        ]

        return image_list

    # ==================================================================================
    # docker ps --all --format :
    #
    _ps_format_list = [
        Format(name="image", format_string="{{.Image}}"),
        Format(name="id", format_string="{{.ID}}"),
        Format(name="name", format_string="{{.Names}}"),
        Format(name="status", format_string="{{.Status}}"),
        Format(name="created", format_string="{{.CreatedAt}}"),
        Format(name="size", format_string="{{.Size}}"),
        Format(name="ports", format_string="{{.Ports}}"),
    ]
    _ps_format_string = Format.join_format_list(_ps_format_list)
    ps_docker_cmd = f"docker ps --all --format '{_ps_format_string}'"

    @classmethod
    def ps(cls, host):
        """Get a list of container properties on the specified host

        Args:
            host(Host): A host object with the attribute "docker_env".

        Returns:
            container_list (list[dict]): A list containing a dictionary 
                for each image on the host. The dictionary is keyed from 
                the name property of the _ps_format_list.
        """
        # each line contains information about a container
        try:
            ps_docker_cmd_output = (
                cls.run_docker_cmd(cmd=cls.ps_docker_cmd, env=host.docker_env)
                .stdout.decode("utf-8")
                .strip()
                .split("\n")
            )
            no_containers = ps_docker_cmd_output == [""]
            if no_containers:
                raise ValueError

        except (AttributeError, ValueError):
            ps_docker_cmd_output = []

        # convert each line to a dictionary keyed by _ps_format_list
        container_list = [
            Format.format_output_to_dict(cls._ps_format_list, line)
            for line in ps_docker_cmd_output
        ]
        return container_list

    # ==================================================================================
    # docker inspect {container_name}
    #
    @classmethod
    def inspect_container(cls, container):
        """Get detailed information about a container

        This information is used to augment the information from the 
        ps command.

        Args:
            container (Container): Container needs a property "name" 
                that corresponds to the name of the container and can be 
                used in the docker inspect command.

        Returns:
            docker_inspect_dict(dict): A dictionary of container properties.
        """
        cmd = f"docker inspect {container.name}"
        docker_inspect_output = cls.run_docker_cmd(
            cmd, env=container.host.docker_env
        ).stdout.decode("utf-8")
        docker_inspect_dict = json.loads(docker_inspect_output)[0]
        return docker_inspect_dict


class Container(object):
    """Representation of a Docker container

    Attributes:
        name (str)
            Container name
        image (str)
            Image ID.
        properties:
            image (str)
                Image ID.
            id (str)
                Container id.
            name (str)
                Container name.
            status (str)
                Container status.
            created (str)
                Time when the container was created.
            size (str)
                Size of container.
            port (str)
                Exposed ports.
        host (Host)
            A reference to the container's host.
        inspect_dict (dict)
            Information from docker inspect.
        link (str)
            link to web server of container.
        image_id (str)
            full id of parent image.

    """

    def __init__(self, properties, host):
        """
        Args: 
            properties (dict): Properties derived from a 'docker ps' cmd
            host (Host): A reference to the container's host.
        """
        self.name = properties["name"]
        self.image = properties["image"]
        self.properties = properties
        self.host = host
        self.inspect_dict = self._inspect_container()
        self.link = self._get_link()
        self.image_id = self._get_image_id()

    def _inspect_container(self):
        """Get information from 'docker inspect'
        """
        return Docker.inspect_container(self)

    def _get_link(self):
        """Construct a link to the container

        Use info from 'docker inspect' to create links to running containers
        """
        # inspect_dict = Docker.inspect_container(self)
        inspect_dict = self.inspect_dict

        # Port
        try:
            port = inspect_dict["HostConfig"]["PortBindings"]["80/tcp"][0]["HostPort"]
        except (KeyError, TypeError):
            port = "____"

        # Status
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

    def _get_image_id(self):
        return self.inspect_dict["Image"]

    def __str__(self):
        cols = (
            "{padded_name:<{NAME}}"
            "{link:<{LINK}}"
            "{id:<{ID}}"
            "{status:<{STATUS}}"
            "{no_size:<{SIZE}}"
        )
        container_string = Colors.container(
            cols.format(
                **self.properties,
                **Inventory.columns,
                padded_name=" " * 4 + f"{self.name}",
                link=self.link,
                no_size="",
            )
        )
        return container_string

    def __repr__(self):
        return f"{self.__class__.__name__}: {self.name}"


class Image(object):
    """Representation of a Docker image

    Attributes:
        name (str): Combination of image and tag, {image:tag}.
        properties:
            image (str): Image repository.
            tag (str): Image tag.
            id (str): Image ID
            created (str): Elapsed time since the image was created
            size (str): Image disk size
            name (str): Combination of image and tag, {image:tag}.
    """

    def __init__(self, image_properties):
        """
        Args:
            image_properties (Dict): Output of 'docker images'.
                - image (str): Image repository.
                - tag (str): Image tag.
                - id (str): Image ID
                - created (str): Elapsed time since the image was created
                - size (str): Image disk size
        """
        self.properties = self._get_properties(image_properties)
        self.name = self.properties["name"]
        self.id = self.properties["id"]

    def _get_properties(self, properties):
        name = "{image}:{tag}".format(**properties)
        properties["name"] = name
        properties["id_trunc"] = properties["id"].split(":")[1][:12]
        return properties

    def __str__(self):
        cols = (
            "{name:<{NAME}}"
            "{no_link:<{LINK}}"
            "{id_trunc:<{ID}}"
            "{created:<{STATUS}}"
            "{size:<{SIZE}}"
        )
        return cols.format(**self.properties, **Inventory.columns, no_link="")

    def __repr__(self):
        return f"{self.__class__.__name__}: {self.name}"


class Host(object):
    """The representation of a single machine

    Encompasses all the information regarding images and their 
    associated containers on a single machine. This information is 
    accessed by the string representation of Host, e.g. str(Host).

    Attributes:
        name (str): Arbitrary name for the machine
        properties (dict): Other relevant information about the machine.
        docker_env (dict): Environment variable necessary to run docker 
            commands on the machine.
        image_list (List[Image]): A list of Image objects. The image
            objects have information about that image.
        container_list (List[Container]): A list of Container objects. 
            The container objects have information about that container.
        host_inventory (OrderedDict): The host_inventory relates the 
            images on a host to the containers created from that image.
    """

    def __init__(self, kernel, images=True, containers=True, inventory=True):
        """
        Args:
            kernel (dict): Contains three keys:
                - name (str): Arbitrary name for machine
                - properties (dict): Other relevant information about 
                      the machine.
                - env (dict): Environment variables necessary to run 
                      docker commands on the machine.
            images (bool): Should images be processed?
            containers (bool): Should containers be processed?
            inventory (bool): Should the images and containers be 
                parsed into a host inventory?
        """
        self.name = kernel["name"]
        self.properties = kernel["properties"]
        self.docker_env = self._get_docker_env(kernel)

        if images or inventory:
            self.image_list = self._list_images()
        if containers or inventory:
            self.container_list = self._list_containers()
        if inventory:
            self.host_inventory = self._merge_items()

    # ----------------------------------------------------------------------------------
    # Environment properties to run remote docker commands
    #
    def _get_docker_env(self, kernel):
        """Create the environment variables for remote docker commands

        Create the environment variables needed to run docker commands
        on the specified machine.
        """
        if kernel["name"] == "localhost":
            env = os.environ.copy()
            env.update(kernel["env"])
            return env
            #return kernel["env"]
        else:
            env = os.environ.copy()
            env.update(kernel["env"])
            return env

    # ----------------------------------------------------------------------------------
    # Images / Containers
    #
    def _list_images(self):
        """Create image list

        Create image objects for all images on this host. 
        'Docker.images' runs 'docker images' and parses the output into 
        a list of image properties. Those properties are used to create 
        an Image object.
        """
        image_list = [Image(properties) for properties in Docker.images(self)]
        return image_list

    def _list_containers(self):
        """Create container list

        Create container objects for all containers on this host. 
        'Docker.ps' runs 'docker ps' and parses the output into 
        a list of container properties. Those properties are used to 
        create a Container object.
        """
        container_list = [Container(properties, self) for properties in Docker.ps(self)]
        return container_list

    # ----------------------------------------------------------------------------------
    # Inventory
    #
    def _merge_items(self):
        """Associate containers with the images used to create them

        localhost-----------------------------------------------------------
        NAME           LINK                  ID           STATUS      SIZE
        foo_dev:latest                       d0ddcf31e8f1 6 days ago  1.75GB
            foo_dev_1  http://localhost:8001 ae13adbe413c Up 28 hours
        --------------------------------------------------------------------

        In the sample output above you can see that foo_dev_1 is 
        indented under foo_dev:latest. From this we can see that 
        the container foo_dev_1 was created from the image 
        foo_dev:latest. That association is created here.

        Returns:
            host_inventory (OrderedDict[id -> properties]):
                id (str): Unique image id
                properties (Dict):
                    properties.image: Image object
                    properties.container_list: List[Container]: List
                        of containers associated with properties.image.
        """
        # Set up the top level structure of host_inventory.
        # For each image create an entry in a dictionary that is
        # keyed by image.id and whose value is another dictionary
        # with keys image and container_list
        host_inventory = OrderedDict(
            (image.id, dict(image=image, container_list=[]))
            for image in self.image_list
        )

        # For each container, use the container.image_id property to
        # add it to the appropriate container list created above.
        for container in self.container_list:
            host_inventory[container.image_id]["container_list"].append(container)

        return host_inventory

    # ----------------------------------------------------------------------------------
    # String: formatted multiline output
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

    # ----------------------------------------------------------------------------------
    # Repr
    #
    def __repr__(self):
        return f"{self.__class__.__name__}: {self.name}"


class Inventory(object):
    """Create a list of all images and containers

    Tool to list all containers and images on your localhost and the 
    remote hosts listed in $HOME/.vscode/settings.json. The list is 
    built by the string representation of the object, i.e. str(Inventory).

    Attributes
        columns (OrderedDict): 
            A mapping of column name to column 
            length. Determines the output of str(Inventory)
        header (str): 
            Formats the columns into a single output string
        line_len (int): 
            Total length of header.
        hosts (List[Host]): 
            A list of host objects. The host objects 
            have information about images and containers on that host.

    """

    # output columns
    columns = OrderedDict(NAME=34, LINK=43, ID=17, STATUS=30, SIZE=10)
    header = "".join(
        ["{title:<{width}}".format(title=k, width=v) for k, v in columns.items()]
    )
    line_len = sum(columns.values())

    def __init__(self, localhost=True, remote=False):
        """
        Args:
            localhost (bool): List images and containers on localhost.
            remote (bool): List images and containers on remote hosts.
        """
        hosts = []
        settings = {}
        # Use a threadpool to build each host in parallel.
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            if localhost:
                local = Settings.get_local_kernal(settings)
                future = executor.submit(Host, local)
                hosts.append(future)

            if remote:
                for remote in Settings.get_remote_kernal_list(settings):
                    future = executor.submit(Host, remote)
                    hosts.append(future)

        self.hosts = [host.result() for host in hosts]

    def __str__(self):
        lines = []
        for host in self.hosts:
            lines.append(Colors.host(f"{host.name: <{self.line_len}}"))
            lines.append(Colors.header(self.header))
            lines.append(str(host))

        return "\n".join(lines)

    def __repr__(self):
        host_list = ", ".join([h.name for h in self.hosts])
        return f"Inventory({host_list})"


def main(localhost=True, remote=True):
    inventory = Inventory(localhost, remote)
    print(inventory)


if __name__ == "__main__":
    main()
