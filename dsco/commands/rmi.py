"""Remove a docker image with 'docker rmi ...'

With no flags, 'dsco rmi' will remove the dev image. To remove a 
specific image add the appropriate flag:

    - :code:`--dev`
    - :code:`--prod`
    - :code:`--debug`

Remove all the images with :code:`--all`.

Before an image can be removed, all containers created from that image 
need to be deleted. To force the deletion of all associated containers, 
you can add the :code:`--force` option.
"""
import os
from pathlib import Path
import subprocess
import yaml
from dsco.commands import rm

cmd_name = Path(__file__).stem


def add_subparser(subparsers):
    sub = subparsers.add_parser(cmd_name, help="remove images")
    sub.add_argument("--dev", action="store_true", help="remove dev")
    sub.add_argument("--prod", action="store_true", help="remove prod")
    sub.add_argument("--debug", action="store_true", help="remove debug")
    sub.add_argument("--all", action="store_true", help="remove dev, prod, and debug")
    sub.add_argument(
        "--force", action="store_true", help="remove corresponding containers"
    )


def run_cmd(args, conf):
    if conf["proj_root"]:
        if args.force:
            # remove associated containers
            rm.run_cmd(args, conf)

        no_flag = not any([args.dev, args.prod, args.debug, args.all])
        flag_list = [
            # (service, service_flag)
            ("dev", args.dev or args.all or no_flag),
            ("prod", args.prod or args.all),
            ("debug", args.debug or args.all),
        ]
        flagged_service_filter = lambda x: x[1]

        proj_name = conf["pyproject"]["tool"]["poetry"]["name"]

        force = "--force" if args.force else ""
        
        for service, _ in filter(flagged_service_filter, flag_list):
            cmd = f"docker rmi {force} {proj_name}_{service}"
            print(cmd)
            subprocess.run(cmd, shell=True)

    else:
        print("No project found.")


def add_dispatch(dispatcher):
    dispatcher[cmd_name] = run_cmd
