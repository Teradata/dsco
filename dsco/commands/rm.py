"""Remove a running or stopped container with 'docker rm -f ...'

With no flags, 'dsco rm' will remove the dev container. To remove a 
specific container add the appropriate flag:

    - :code:`--dev`
    - :code:`--prod`
    - :code:`--debug`

Remove all the containers with --all.
"""
import os
from pathlib import Path
import subprocess
import yaml
from dsco.helpers import get_container

cmd_name = Path(__file__).stem


def add_subparser(subparsers):
    sub = subparsers.add_parser(cmd_name, help="remove containers")
    sub.add_argument("--dev", action="store_true", help="remove dev")
    sub.add_argument("--prod", action="store_true", help="remove prod")
    sub.add_argument("--debug", action="store_true", help="remove debug")
    sub.add_argument("--all", action="store_true", help="remove dev, prod, and debug")


def run_cmd(args, conf):
    if conf["proj_root"]:
        no_flag = not any([args.dev, args.prod, args.debug, args.all])
        flag_list = [
            # (service, service_flag)
            ("dev", args.dev or args.all or no_flag),
            ("prod", args.prod or args.all),
            ("debug", args.debug or args.all),
        ]
        flagged_service_filter = lambda x: x[1]

        proj_name = conf["pyproject"]["tool"]["poetry"]["name"]

        for service, _ in filter(flagged_service_filter, flag_list):
            get_container_cmd = get_container(proj_name, service)
            cmd = f"docker rm -f $({get_container_cmd})"
            print(cmd)
            subprocess.run(cmd, shell=True)

    else:
        print("No project found.")


def add_dispatch(dispatcher):
    dispatcher[cmd_name] = run_cmd
