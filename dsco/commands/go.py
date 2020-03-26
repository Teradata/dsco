"""go: A quickstart command to build a container and open a browser

'dsco go' is a quickstart method to create a container and open the 
web page interface to the container.

Options
    --dev: dev container
    --prod: prod container
    --debug: debug container (unlikely to have a running server)

Options are cumulative, meaning --dev --prod will launch and open
both the dev and prod containers.
"""
import os
from pathlib import Path

import yaml
from dsco.commands import up
from dsco.helpers import add_timer
import webbrowser

# from dsco.commands.ls import Colors as colors

cmd_name = Path(__file__).stem


def add_subparser(subparsers):
    sub = subparsers.add_parser(
        cmd_name, help="Build containers, then open the web page interface."
    )
    sub.add_argument("--dev", action="store_true", help="dev container")
    sub.add_argument("--prod", action="store_true", help="prod container")
    sub.add_argument("--debug", action="store_true", help="debug container")
    sub.add_argument("--all", action="store_true", help="all containers")


@add_timer(cmd_name)
def run_cmd(args, conf):
    # build and launch the containers
    up.run_cmd(args, conf)

    # open the web page interface
    if conf["proj_root"]:
        no_flags = not any([args.dev, args.prod, args.debug])
        flag_list = [
            ("dev", args.dev or no_flags or args.all),  # default option
            ("prod", args.prod or args.all),
            ("debug", args.debug or args.all),
        ]
        flagged_service_filter = lambda x: x[1]

        services_conf = conf["docker_compose_yaml"]["services"]

        for service, _ in filter(flagged_service_filter, flag_list):
            proj_port = services_conf[service]["ports"][0].split(":")[0]
            webbrowser.open(f"http://localhost:{proj_port}", new=2, autoraise=True)


def add_dispatch(dispatcher):
    dispatcher[cmd_name] = run_cmd
