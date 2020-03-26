"""reports: view and update reports created in docs/reports

Uses sphinx to (re)generate the reports created in docs/reports.
This creates static html that can be viewed 
through the containers web page or github pages.

Currently this only targets the dev container.

Usage:
    'dsco reports': open a webbrowser on localhost/reports/
    'dsco reports [-g, --generate]': update reports
"""
import os
from pathlib import Path
import subprocess
import webbrowser
import yaml
from dsco.helpers import get_container, get_port

cmd_name = Path(__file__).stem


def add_subparser(subparsers):
    sub = subparsers.add_parser(
        cmd_name, help="view and update reports in the dev container"
    )
    sub.add_argument(
        "-g",
        "--generate",
        action="store_true",
        help="(re)generate reports in static html",
    )


def run_cmd(args, conf):
    if conf["proj_root"]:
        if args.generate:
            proj_name = conf["pyproject"]["tool"]["poetry"]["name"]
            bash_cmd = "bash -c 'cd /srv/docs/reports/source && make html'"
            container_name = get_container(proj_name, "dev")
            cmd = f"docker exec -it $({container_name}) {bash_cmd}"
            print(cmd)
            subprocess.run(cmd, shell=True)

        else:
            proj_port = get_port(conf, "dev")
            url = f"http://localhost:{proj_port}/reports/"
            webbrowser.open(url, new=2, autoraise=True)


    else:
        print("No project found.")


def add_dispatch(dispatcher):
    dispatcher[cmd_name] = run_cmd
