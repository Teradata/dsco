"""up: Create and launch specified containers

Runs 'docker-compose up -d ...' for the specified process. 
Options: --dev, --prod, --all

If the --debug flag is provided, only the debug container is launched. 
Even if --dev or --prod flags are provided.

Otherwise (i.e. no --debug):
    -- dev, all, or no flags  |  dev container is launched 
    -- prod or all            |  prod container is launched
"""
import os
from pathlib import Path
import subprocess
import yaml
from dsco.helpers import add_timer

cmd_name = Path(__file__).stem


def add_subparser(subparsers):
    sub = subparsers.add_parser(cmd_name, help="create and launch containers")
    sub.add_argument("--dev", action="store_true", help="dev container")
    sub.add_argument("--prod", action="store_true", help="prod container")
    sub.add_argument(
        "--debug",
        action="store_true",
        help="bring up base container without running ansible",
    )
    sub.add_argument("--all", action="store_true", help="dev and prod containers")


@add_timer(cmd_name)
def run_cmd(args, conf):
    if conf["proj_root"]:
        # Flag logic
        no_flags = not any([args.dev, args.prod, args.debug, args.all])
        service_list = [
            # (service, flag)
            ("dev", (args.dev or args.all or no_flags) and not args.debug),
            ("prod", (args.prod or args.all) and not args.debug),
            ("debug", args.debug),
        ]
        services_str = " ".join([service for service, flag in service_list if flag])

        cmd = f"docker-compose up -d {services_str}"
        print(cmd)
        subprocess.run(cmd, cwd=conf["proj_root"], shell=True)

    else:
        print("No project found.")


def add_dispatch(dispatcher):
    dispatcher[cmd_name] = run_cmd
