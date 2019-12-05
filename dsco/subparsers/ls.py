import os
from pathlib import Path
import subprocess
import yaml
from dsco.helpers import docker_ps

cmd_name = Path(__file__).stem


def add_cmd(subparsers):
    cmd = subparsers.add_parser(cmd_name, help="list containers")
    cmd.add_argument(
        "-r", "--remote",
        action="store_true",
        help="list remote containers using docker-machine",
    )


def run_cmd(args, conf):
    docker_ps(remote=args.remote)


def add_dispatch(dispatcher):
    dispatcher[cmd_name] = run_cmd
