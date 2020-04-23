"""code: launch vs-code insiders with the appropriate environment

'dsco code' will launch vs-code locally. From there you can attach 
    to a locally running container.

'dsco code -r [remote machine]' or 'dsco code --remote [remote machine]' 
    will launch vs-code with the appropriate environment variables to 
    connect to the remote machine. You should then be able to connect 
    to containers running there.
"""

import os
from sys import exit
from pathlib import Path
import subprocess
import yaml
from dsco.commands.ls import Docker, Host, Inventory


cmd_name = Path(__file__).stem
VSCODE = "code"

def add_subparser(subparsers):
    sub = subparsers.add_parser(cmd_name, help="launch vs-code")
    sub.add_argument(
        "-r", "--remote", help="connect to a container with docker-machine"
    )


def run_cmd(args, conf):
    # set up base environment
    env = {**os.environ}

    # are we running local or remote?
    if args.remote:
        try:
            machine_name = args.remote
            machine_list = Inventory.remote_list()
            machine = next(
                machine for machine in machine_list if machine_name == machine["name"]
            )
        except StopIteration:
            known_machines = [remote["name"] for remote in machine_list]
            print(f"{machine} not found in $HOME/.dsco/settings.json")
            print(f"known machines: {known_machines}")
            # Stop here (but without a big error message)
            exit(1)
        else:
            machine_env = machine["env"]
            env.update(**machine_env)

    cmd = f"{VSCODE} --new-window"
    print(cmd)
    subprocess.run(cmd, shell=True, env=env)


def add_dispatch(dispatcher):
    dispatcher[cmd_name] = run_cmd


if __name__ == "__main__":
    # setup local argparse for testing
    import argparse

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="cmd")
    add_subparser(subparsers)

    args = parser.parse_args()

    # Nothing needed from conf
    conf = dict()

    run_cmd(args, conf)
