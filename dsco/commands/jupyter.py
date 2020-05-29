"""Provide the link to the jupyter notebook server including login token
"""
import os
from pathlib import Path
import subprocess
import yaml
from dsco.helpers import get_container
from dsco.local_options import Settings as settings

cmd_name = Path(__file__).stem

OKBLUE = "\033[94m"
REVERSED = "\u001b[7m"
UNDERLINE = "\033[4m"
ENDC = "\033[0m"


def add_subparser(subparsers):
    sub = subparsers.add_parser(cmd_name, help="link to jupyter notebook")
    sub.add_argument("--dev", action="store_true", help="dev")
    sub.add_argument("--prod", action="store_true", help="prod")
    sub.add_argument("--debug", action="store_true", help="debug")
    sub.add_argument("--all", action="store_true", help="dev, prod, and debug")


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

        local_settings = settings.get_local_kernal()
        try:
            local_ip = local_settings["properties"]["ip"]
        except KeyError:
            local_ip = "localhost"

        for service, _ in filter(flagged_service_filter, flag_list):
            get_container_cmd = get_container(proj_name, service)
            ports = conf["docker_compose_yaml"]["services"][service]["ports"]
            port = ports[0].split(":")[0]
            cmd = f"docker exec -it $({get_container_cmd}) jupyter notebook list"
            print(REVERSED + f"{proj_name + '_' + service:<88}" + ENDC)
            print(OKBLUE + cmd + ENDC)
            # expected output of cmd:
            #     Currently running servers:
            #     http://0.0.0.0:8888/notebook/?token=<token> :: /srv
            try:
                result = (
                    subprocess.run(cmd, shell=True, capture_output=True)
                    .stdout.decode("utf-8")
                    .strip()
                    .split("\n")
                )[-1].split()[0]
            except IndexError:
                print(f"No server found.")
            else:
                token = result.split("=")[-1]
                print(f"http://{local_ip}:{port}/notebook/?token={token}")

    else:
        print("No project found.")


def add_dispatch(dispatcher):
    dispatcher[cmd_name] = run_cmd
