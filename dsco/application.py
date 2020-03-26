"""A tool to create, manage, and destroy data science development containers.

Uses the parser from :py:mod:`dsco.options` to read the command line 
options (args). Creates a conf dictionary to load project 
information (based on current path).
Runs the function found by the :code:`cmd --> run_cmd` mapping in 
dispatcher, passing both args and conf. i.e. 
:code:`run_cmd(args, conf)`.
"""
import argparse
from pathlib import Path
from .options import parser, dispatcher
from .helpers import find_proj_root, get_pyproject, get_docker_compose_conf


def main():
    # ----------------------------------------------------------------------------------
    # args: get command line options. 
    # ----------------------------------------------------------------------------------
    #     the parser is defined in 'options.py'
    #     args is a Namespace. dsco ls -r would return:
    #         - args.cmd = ls
    #         - args.remote = True
    #
    args = parser.parse_args()

    # ----------------------------------------------------------------------------------
    # conf (dict): configuration information
    # ----------------------------------------------------------------------------------
    #     - install_root (Path): location of dsco install
    #     - cwd (Path): directory dsco was called from
    #     - proj_root: The directory on the current path that contains pyproject.toml.
    #           If pyproject.toml is not on current path, value = ""
    #
    #     if proj_root was found:
    #         We excect to find the files pyproject.toml and docker-compose.yml
    #         - pyproject (dict): pyproject.toml config
    #         - docker_compose_yaml (dict): docker-compose.yml config
    #     else values are {}
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
        conf["docker_compose_yaml"]={}

    # run method from dispatcher based on args and conf
    dispatcher[args.cmd](args, conf)


if __name__ == "__main__":
    main()