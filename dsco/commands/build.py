"""Build a container image

:code:`dsco build` creates images by running docker-compose from the project 
root directory. By default :code:`dsco build` will build the dev container. 

Options
    - :code:`-- dev`
    - :code:`-- prod`
    - :code:`-- all`
    - :code:`-- debug`

The dev container will be built when:
    - :code:`-- dev == True`
    - :code:`-- all == True`
    - no flags are given

The prod container will be built when:
    - :code:`-- prod == True`
    - :code:`-- all == True`

The debug container will be built when:
    - :code:`-- debug == True`
    - :code:`-- all == True`
"""
import os
from ..helpers import add_timer
from pathlib import Path
import subprocess
import yaml
import time

cmd_name = Path(__file__).stem


def add_subparser(subparsers):
    sub = subparsers.add_parser(cmd_name, help="build images. No flag builds dev.")
    sub.add_argument("--dev", action="store_true", help="build dev image")
    sub.add_argument("--prod", action="store_true", help="build prod image")
    sub.add_argument("--debug", action="store_true", help="build debug image")
    sub.add_argument("--all", action="store_true", help="build all images")


@add_timer(cmd_name)
def run_cmd(args, conf):
    # only run if there's a project on our path
    if conf["proj_root"]:
        no_flag = not any([args.dev, args.prod, args.debug])
        dev_flag = args.dev or args.all or no_flag
        prod_flag = args.prod or args.all
        debug_flag = args.dev or args.all

        service_list = [("dev", dev_flag), ("prod", prod_flag), ("debug", debug_flag)]
        service_str = " ".join([service for (service, flag) in service_list if flag])

        docker_cmd = f"docker-compose build {service_str}"

        print(docker_cmd)
        subprocess.run(docker_cmd, cwd=conf["proj_root"], shell=True)

    else:
        print("No project found.")


def add_dispatch(dispatcher):
    dispatcher[cmd_name] = run_cmd
