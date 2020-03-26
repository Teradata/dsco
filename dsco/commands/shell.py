"""shell: Open a shell inside the specified container

If not container is specified, 
"""
import os
from pathlib import Path
import subprocess
import yaml
from dsco.helpers import get_container

cmd_name = Path(__file__).stem


def add_subparser(subparsers):
    sub = subparsers.add_parser(cmd_name, help="start shell in container")
    sub.add_argument("--dev", action="store_true", help="attach to dev")
    sub.add_argument("--prod", action="store_true", help="attach to prod")
    sub.add_argument("--debug", action="store_true", help="attach to debug")


def run_cmd(args, conf):
    if conf["proj_root"]:
        proj_name = conf["pyproject"]["tool"]["poetry"]["name"]
        bash_cmd = """bash -c 'cd /srv && exec "${SHELL:-sh}"'"""

        if args.prod:
            container_name = get_container(proj_name, "prod")
        elif args.debug:
            container_name = get_container(proj_name, "debug")
        else:
            container_name = get_container(proj_name, "dev")

        cmd = f"docker exec -it $({container_name}) {bash_cmd}"
        print(cmd)
        subprocess.run(cmd, shell=True)

    else:
        print("No project found.")


def add_dispatch(dispatcher):
    dispatcher[cmd_name] = run_cmd
