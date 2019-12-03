import os
import toml
from pathlib import Path
import yaml


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
    with open(str(p), 'r') as f:
        yaml_file = yaml.load(f, Loader=yaml.Loader)
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