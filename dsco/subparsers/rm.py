import os
from pathlib import Path
import subprocess
import yaml
from dsco.helpers import get_container

cmd_name = Path(__file__).stem


def add_cmd(subparsers):
    cmd = subparsers.add_parser(cmd_name, help="remove containers")
    cmd.add_argument("--dev", action="store_true", help="remove dev")
    cmd.add_argument("--prod", action="store_true", help="remove prod")
    cmd.add_argument("--all", action="store_true", help="remove dev and prod")


def run_cmd(args, conf):
    if conf["proj_root"]:
        dev_flag = args.dev or args.all
        prod_flag = args.prod or args.all

        proj_name = conf["pyproject"]["tool"]["poetry"]["name"]

        if prod_flag:
            container_name = get_container(proj_name, "prod")
            cmd = f"docker rm -f $({container_name})"
            print(cmd)
            subprocess.run(cmd, shell=True)

        only_prod_flag = not dev_flag and prod_flag
        if not only_prod_flag:
            container_name = get_container(proj_name, "dev")
            cmd = f"docker rm -f $({container_name})"
            print(cmd)
            subprocess.run(cmd, shell=True)

    else:
        print("No project found.")


def add_dispatch(dispatcher):
    dispatcher[cmd_name] = run_cmd
