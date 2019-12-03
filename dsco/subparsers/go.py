import os
from pathlib import Path
import subprocess
import yaml

cmd_name = "go"


def add_cmd(subparsers):
    cmd = subparsers.add_parser(cmd_name, help="create and launch containers")
    cmd.add_argument("--dev", action="store_true", help="dev container only")
    cmd.add_argument("--prod", action="store_true", help="prod container only")
    cmd.add_argument("--all", action="store_true", help="dev and prod containers")


def run_cmd(args, conf):
    if conf["proj_root"]:
        dev_flag = args.dev or args.all
        prod_flag = args.prod or args.all

        services_conf = conf["docker_compose_yaml"]["services"]

        if prod_flag:
            cmd = "docker-compose up -d prod"
            subprocess.run(cmd, cwd=conf["proj_root"], shell=True)
            proj_port = services_conf["prod"]["ports"][0].split(":")[0]

        only_prod_flag = not dev_flag and prod_flag
        if not only_prod_flag:
            cmd = "docker-compose up -d dev"
            subprocess.run(cmd, cwd=conf["proj_root"], shell=True)
            proj_port = services_conf["dev"]["ports"][0].split(":")[0]

        subprocess.run(f"python -m webbrowser http://localhost:{proj_port}", shell=True)
    else:
        print("No project found.")


def add_dispatch(dispatcher):
    dispatcher[cmd_name] = run_cmd
