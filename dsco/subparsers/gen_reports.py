import os
from pathlib import Path
import subprocess
import yaml
from dsco.helpers import get_container

cmd_name = "gen_reports"


def add_cmd(subparsers):
    subparsers.add_parser(cmd_name, help="(re)generate reports in static html")


def run_cmd(args, conf):
    if conf["proj_root"]:
        proj_name = conf["pyproject"]["tool"]["poetry"]["name"]
        bash_cmd = "bash -c 'cd /srv/reports && make html'"
        container_name = get_container(proj_name, "dev")
        cmd = f"docker exec -it $({container_name}) {bash_cmd}"

        subprocess.run(cmd, shell=True)

    else:
        print("No project found.")


def add_dispatch(dispatcher):
    dispatcher[cmd_name] = run_cmd
