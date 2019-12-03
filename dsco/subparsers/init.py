import os
from pathlib import Path
from cookiecutter.main import cookiecutter

cmd_name = "init"

def add_cmd(subparsers):
    subparsers.add_parser(cmd_name, help='create a new project')

def run_cmd(args, conf):
    proj_template = conf["install_root"].parent / 'project_template'
    output_dir = conf["cwd"]
    print(f"Using template: {proj_template}")
    print(f"Creating project in {output_dir}")
    cookiecutter(str(proj_template), output_dir=str(output_dir))

def add_dispatch(dispatcher):
    dispatcher[cmd_name] = run_cmd
