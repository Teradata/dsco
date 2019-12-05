import os
from pathlib import Path
import subprocess
import yaml

cmd_name = Path(__file__).stem


def add_cmd(subparsers):
    cmd = subparsers.add_parser(cmd_name, help="build containers")
    cmd.add_argument("--dev", action="store_true", help="build dev container")
    cmd.add_argument("--prod", action="store_true", help="build prod container")
    cmd.add_argument("--all", action="store_true", help="build dev and prod containers")


def run_cmd(args, conf):
    if conf["proj_root"]:
        dev_flag = args.dev or args.all
        prod_flag = args.prod or args.all

        if prod_flag:
            subprocess.run(
                "docker-compose build prod", cwd=conf["proj_root"], shell=True
            )

        only_prod_flag = not dev_flag and prod_flag
        if not only_prod_flag:
            subprocess.run(
                "docker-compose build dev", cwd=conf["proj_root"], shell=True
            )

    else:
        print("No project found.")


def add_dispatch(dispatcher):
    dispatcher[cmd_name] = run_cmd
