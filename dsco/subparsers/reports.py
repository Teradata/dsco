import os
from pathlib import Path
import subprocess
import yaml
from dsco.helpers import get_container

cmd_name = Path(__file__).stem


def add_cmd(subparsers):
    cmd = subparsers.add_parser(cmd_name, help="view and update reports")
    cmd.add_argument(
        "-g",
        "--generate",
        action="store_true",
        help="(re)generate reports instatic html",
    )


def run_cmd(args, conf):
    if conf["proj_root"]:
        if args.generate:
            proj_name = conf["pyproject"]["tool"]["poetry"]["name"]
            bash_cmd = "bash -c 'cd /srv/reports && make html'"
            container_name = get_container(proj_name, "dev")
            cmd = f"docker exec -it $({container_name}) {bash_cmd}"

            subprocess.run(cmd, shell=True)
        else:
            services_conf = conf["docker_compose_yaml"]["services"]
            proj_port = services_conf["dev"]["ports"][0].split(":")[0]
            subprocess.run(
                f"python -m webbrowser http://localhost:{proj_port}/reports/",
                shell=True,
            )

    else:
        print("No project found.")


def add_dispatch(dispatcher):
    dispatcher[cmd_name] = run_cmd
