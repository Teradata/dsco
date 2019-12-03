import os
from pathlib import Path
from cookiecutter.main import cookiecutter
from dsco.helpers import get_container
import subprocess

cmd_name = "restart_flask"

def add_cmd(subparsers):
    cmd = subparsers.add_parser(cmd_name, help='restart flask (dev)')
    cmd.add_argument("--dev", action="store_true", help="restart dev only")
    cmd.add_argument("--prod", action="store_true", help="restart prod only")
    cmd.add_argument("--all", action="store_true", help="restart dev and prod")

def run_cmd(args, conf):
    if conf["proj_root"]:
        dev_flag = args.dev or args.all
        prod_flag = args.prod or args.all

        proj_name = conf["pyproject"]["tool"]["poetry"]["name"]
        bash_cmd = 'bash -c "supervisorctl restart uwsgi && supervisorctl status"'

        if prod_flag:
            container_name = get_container(proj_name, "prod")
            cmd = f"docker exec -it $({container_name}) {bash_cmd}"
            subprocess.run(cmd, shell=True)

        only_prod_flag = prod_flag and not dev_flag
        if not only_prod_flag:
            container_name = get_container(proj_name, "dev")
            cmd = f"docker exec -it $({container_name}) {bash_cmd}"
            subprocess.run(cmd, shell=True)
    else:
        print("No project found.")

def add_dispatch(dispatcher):
    dispatcher[cmd_name] = run_cmd
