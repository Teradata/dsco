import os
import toml
from pathlib import Path
import yaml
import subprocess
from collections import namedtuple


Machine = namedtuple("Machine", "name url")
localhost = Machine("localhost", "localhost")


# search for pyproject.toml
def find_proj_root(path):
    p = Path(path)
    proj_root = ""
    if "pyproject.toml" in os.listdir(p):
        proj_root = path
    elif path != Path("/"):
        proj_root = find_proj_root(p.parent)

    return proj_root


def get_pyproject(path):
    file = os.path.join(path, "pyproject.toml")
    with open(file) as conffile:
        config = toml.loads(conffile.read())
    return config


def get_docker_compose_conf(path):
    p = Path(path) / "docker-compose.yml"
    if p.exists():
        with open(str(p), "r") as f:
            yaml_file = yaml.load(f, Loader=yaml.Loader)
    else:
        yaml_file = {}
    return yaml_file


def get_container(proj_name, service):
    name_filter = f"--filter 'label=com.docker.compose.project={proj_name}'"
    service_filter = f"--filter 'label=com.docker.compose.service={service}'"
    _format = "--format {{.Names}}"

    container_name = f"docker ps {name_filter} {service_filter} {_format}"

    return container_name


def update_port(lines, old_port, new_port):
    defined_on_line = lines.index(next(i for i in lines if old_port in i))
    lines[defined_on_line] = lines[defined_on_line].replace(old_port, str(new_port))


def parse_machine(out):
    # out = sdl32266 tcp://sdl32266.labs.teradata.com:2376
    name, url = out.split()
    url = str(url.split("//")[-1].split(":")[0])
    return Machine(name, url)


def list_docker_machines():
    output = (
        subprocess.run(
            'docker-machine ls --format "{{.Name}} {{.URL}}"',
            shell=True,
            capture_output=True,
        )
        .stdout.decode("utf-8")
        .strip()
        .split("\n")
    )

    return [parse_machine(i) for i in output]


def docker_ps_cmd(project="", service="", dsco=False):
    project_filter_template = f'--filter "label=com.docker.compose.project={project}"'
    project_filter = project_filter_template if project else ""

    service_filter_template = f'--filter "label=com.docker.compose.service={service}"'
    service_filter = service_filter_template if service else ""

    dsco_filter_template = f'--filter "label=com.teradata.dsco"'
    dsco_filter = dsco_filter_template if dsco else ""

    filters = f"{project_filter} {service_filter} {dsco_filter}"

    format_flag = '--format "table {{.Names}}\t{{.Status}}\thttp://{{.Ports}}"'

    cmd = f"docker ps {format_flag} {filters} --all"

    return cmd


def docker_ps_output_cleanup(ps_output, machine):
    return (
        ps_output.stdout.decode("utf-8")
        .replace("->", " -> ")
        .replace("0.0.0.0", machine.url)
    )


def _docker_ps(project="", service="", dsco=False, machine=localhost):
    cmd_list = []
    if machine == localhost:
        cmd_list.append(docker_ps_cmd(project=project, service=service, dsco=dsco))
    else:
        cmd_list.append(f'eval "$(docker-machine env {machine.name})"')
        cmd_list.append(docker_ps_cmd())
        cmd_list.append(f'eval "$(docker-machine env -u)"')

    cmd = " && ".join(cmd_list)

    result = subprocess.run(cmd, shell=True, capture_output=True)

    return docker_ps_output_cleanup(result, machine)


def docker_ps(project="", service="", dsco=False, local=True, remote=False):
    if local:
        print("localhost")
        print("---------")
        print(_docker_ps(project, service, dsco))
        print('-'*88)
    
    if remote:
        for machine in list_docker_machines():
            print(machine.name)
            print('-'*len(machine.name))
            print(_docker_ps(machine=machine))
            print('-'*88)
