"""restart: Restart nginx or flask in the dev container

'dsco restart' will restart both the nginx service and the flask service
running inside the development container. To restart just one of those 
use the corresponding flag: --nginx or --flask
"""
import os
from pathlib import Path
from cookiecutter.main import cookiecutter
from dsco.helpers import get_container
import subprocess

cmd_name = Path(__file__).stem


def add_subparser(subparsers):
    sub = subparsers.add_parser(cmd_name, help="restart nginx and flask (dev)")
    sub.add_argument("--flask", action="store_true", help="restart flask")
    sub.add_argument("--nginx", action="store_true", help="restart nginx")


def run_cmd(args, conf):
    if conf["proj_root"]:
        no_flag = not any([args.flask, args.nginx])
        flask_flag = args.flask or no_flag
        nginx_flag = args.nginx or no_flag

        proj_name = conf["pyproject"]["tool"]["poetry"]["name"]

        container_name = get_container(proj_name, "dev")

        if nginx_flag:
            restart_nginx = 'bash -c "service nginx restart"'
            cmd = f"docker exec -it $({container_name}) {restart_nginx}"
            print(cmd)
            subprocess.run(cmd, shell=True)

        if flask_flag:
            restart_flask = (
                'bash -c "supervisorctl restart uwsgi && supervisorctl status"'
            )
            cmd = f"docker exec -it $({container_name}) {restart_flask}"
            print(cmd)
            subprocess.run(cmd, shell=True)

    else:
        print("No project found.")


def add_dispatch(dispatcher):
    dispatcher[cmd_name] = run_cmd
