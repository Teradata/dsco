import os
from pathlib import Path
from cookiecutter.main import cookiecutter
from dsco.helpers import get_container, update_port
import subprocess

cmd_name = "update_port"


def add_cmd(subparsers):
    cmd = subparsers.add_parser(cmd_name, help="update contianer port")
    cmd.add_argument(
        "base_port", type=int, nargs="?", help="by default update dev and prod"
    )
    cmd.add_argument("--dev", type=int, help="update dev port")
    cmd.add_argument("--prod", type=int, help="update prod port")


def run_cmd(args, conf):
    if conf["proj_root"]:
        proj_root = conf["proj_root"]
        proj_services = conf["docker_compose_yaml"]["services"]
        compose_file = Path(proj_root) / "docker-compose.yml"
        lines = compose_file.read_text().split("\n")

        # Defaults
        dev_flag = False
        prod_flag = False

        # set values and flags
        if args.base_port:
            dev_flag = True
            dev_port = args.base_port
            prod_flag = True
            prod_port = dev_port + 1000

        if args.dev:
            dev_flag = True
            dev_port = str(args.dev)

        if args.prod:
            prod_flag = True
            prod_port = str(args.prod)

        # Update docker-compose.yml
        if dev_flag:
            old_dev_port = proj_services["dev"]["ports"][0].split(":")[0]
            update_port(lines, old_dev_port, dev_port)

        if prod_flag:
            old_prod_port = proj_services["prod"]["ports"][0].split(":")[0]
            update_port(lines, old_prod_port, prod_port)

        if dev_flag or prod_flag:
            compose_file.write_text(os.linesep.join(lines), encoding="UTF-8")
        else:
            print("No changes made.")
    else:
        print("No project found.")


def add_dispatch(dispatcher):
    dispatcher[cmd_name] = run_cmd
