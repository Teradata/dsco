import os
from pathlib import Path
import subprocess
import yaml

cmd_name = Path(__file__).stem


def add_cmd(subparsers):
    cmd = subparsers.add_parser(cmd_name, help="create and launch containers")
    cmd.add_argument("--dev", action="store_true", help="dev container only")
    cmd.add_argument("--prod", action="store_true", help="prod container only")
    cmd.add_argument(
        "--debug",
        action="store_true",
        help="bring up base container without running ansible",
    )
    cmd.add_argument("--all", action="store_true", help="dev and prod containers")


def run_cmd(args, conf):
    if conf["proj_root"]:
        # Flag logic
        no_flags = not args.dev and not args.prod and not args.all and not args.debug
        dev_flag = (args.dev or args.all or no_flags) and not args.debug
        prod_flag = (args.prod or args.all) and not args.debug
        debug_flag = args.debug

        if prod_flag:
            cmd = "docker-compose up -d prod"
            subprocess.run(cmd, cwd=conf["proj_root"], shell=True)

        if dev_flag:
            cmd = "docker-compose up -d dev"
            subprocess.run(cmd, cwd=conf["proj_root"], shell=True)

        if debug_flag:
            cmd = "docker-compose up -d debug"
            subprocess.run(cmd, cwd=conf["proj_root"], shell=True)

    else:
        print("No project found.")


def add_dispatch(dispatcher):
    dispatcher[cmd_name] = run_cmd
