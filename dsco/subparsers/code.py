"""launch vs code with the appropriate environment

dsco code 
    --remote -r
"""

import os
from sys import exit
from pathlib import Path
import subprocess
import yaml
from dsco.subparsers.ls import Docker, Host


cmd_name = Path(__file__).stem


def add_cmd(subparsers):
    cmd = subparsers.add_parser(cmd_name, help="launch vs code")
    cmd.add_argument(
        "-r", "--remote", help="connect to a container with docker-machine"
    )


def run_cmd(args, conf):
    host_args = dict(name="", images=False, containers=False, inventory=False)
    if args.remote:
        try:
            machine = args.remote
            machine_list = Docker.ls_machines()
            assert machine in machine_list
        except AssertionError:
            print(f"{machine} must be docker-machine")
            print(f"docker machines: {machine_list}")
            # Stop here (but without a big error message)
            exit(1)
        else:
            host_args["name"] = args.remote
    else:
        host_args["name"] = "localhost"
    
    host = Host(**host_args)

    cmd = "code"
    env = {**os.environ, **host.docker_machine_env}
    subprocess.run(cmd, shell=True, env=env)


def add_dispatch(dispatcher):
    dispatcher[cmd_name] = run_cmd


if __name__ == "__main__":
    # setup local argparse for testing
    import argparse

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="cmd")
    add_cmd(subparsers)

    args = parser.parse_args()

    # Nothing needed from conf
    conf = dict()

    run_cmd(args, conf)
