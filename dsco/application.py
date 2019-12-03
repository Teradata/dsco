"""Create data science containers (dsco)
"""
import argparse
from pathlib import Path
from .options import parser, dispatcher
from .helpers import find_proj_root, get_pyproject, get_docker_compose_conf


def main():
    # get command line options
    args = parser.parse_args()

    # build configuration
    conf = dict(
        install_root=Path(__file__),
        cwd=Path.cwd(), 
        proj_root=find_proj_root(Path.cwd()), 
    )

    if conf["proj_root"]:
        proj_root = conf["proj_root"]
        conf["pyproject"]=get_pyproject(proj_root)
        conf["docker_compose_yaml"]=get_docker_compose_conf(proj_root)
    else:
        conf["pyproject"]={}

    # run method from dispatcher based on args and conf
    dispatcher[args.cmd](args, conf)


if __name__ == "__main__":
    main()