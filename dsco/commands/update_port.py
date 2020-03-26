"""update_port: Update the ports of the specified container

Each container on a host needs to have a unique port. This method will 
make the appropriate updates in the project docker-compose file.

If we just enter one port number (e.g. 'dsco update_port 8000'):
    - the dev port will be set to 8000
    - the prod port will be set to 8000 + 1000 = 9000
    - the debug port will be set to 8000 - 500 = 7500

If we want more control we can use the flag options to set those ports 
to specific values.

Examples
    dsco update_port 8000
        dev: 8000, prod: 9000, debug: 7500

    dsco update_port 8000 --prod 9400
        dev: 8000, prod: 9400, debug: 7500

    dsco update_port --debug 7630
        dev: unchanged, prod: unchanged, debug: 7630

    dsco update_port 8200 --prod 9400 --debug 7630
        dev: 8200, prod: 9400, debug: 7630

    dsco update_port --dev 8200 --debug 7620
        dev: 8200, prod: unchanged, debug: 7620
"""
import os
from pathlib import Path
from cookiecutter.main import cookiecutter
from dsco.helpers import get_container, update_port
import subprocess

cmd_name = Path(__file__).stem


def add_subparser(subparsers):
    sub = subparsers.add_parser(
        cmd_name, help="update container port (container restart required)"
    )
    sub.add_argument(
        "base_port",
        type=int,
        nargs="?",
        help="update ports dev: base_port, prod: base_port+1000, debug: base_port-500",
    )
    sub.add_argument("--dev", type=int, help="update dev port, overwrites base_port")
    sub.add_argument("--prod", type=int, help="update prod port, overwrites base_port")
    sub.add_argument(
        "--debug", type=int, help="update debug port, overwrites base_port"
    )


def run_cmd(args, conf):
    if conf["proj_root"]:
        proj_root = conf["proj_root"]
        proj_services = conf["docker_compose_yaml"]["services"]
        compose_file = Path(proj_root) / "docker-compose.yml"
        file_lines = compose_file.read_text().split("\n")

        # Defaults
        dev_flag, dev_port = False, 0
        prod_flag, prod_port = False, 0
        debug_flag, debug_port = False, 0

        # set values and flags
        if args.base_port:
            dev_flag = True
            dev_port = args.base_port
            prod_flag = True
            prod_port = dev_port + 1000
            debug_flag = True
            debug_port = dev_port - 500

        if args.dev:
            dev_flag = True
            dev_port = str(args.dev)

        if args.prod:
            prod_flag = True
            prod_port = str(args.prod)

        if args.debug:
            debug_flag = True
            debug_port = str(args.debug)

        # combine into modification list
        modification_list = [
            ("dev", dev_port, dev_flag),
            ("prod", prod_port, prod_flag),
            ("debug", debug_port, debug_flag),
        ]
        flagged_modifications = lambda x: x[-1]

        # Update docker-compose.yml per modification list
        for service, new_port, _ in filter(flagged_modifications, modification_list):
            old_port = proj_services[service]["ports"][0].split(":")[0]
            # 'file_lines' is mutated so effects are cumulative
            update_port(file_lines, old_port, new_port)

        # if we made modifications update docker-compose
        if any(filter(flagged_modifications, modification_list)):
            compose_file.write_text(os.linesep.join(file_lines), encoding="UTF-8")
        else:
            print("No changes made.")
    else:
        print("No project found.")


def add_dispatch(dispatcher):
    dispatcher[cmd_name] = run_cmd
