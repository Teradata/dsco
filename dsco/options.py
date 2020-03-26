"""Add commands to the argument parser

The argument parser is what translates the text entered on the command 
line to specific actions. For example, if we enter :code:`dsco init` we 
want our program to create a new project folder populated from our 
project template. 

The form this takes is :code:`dsco [subparser ...]`. Where subparser 
consists of a command plus options. For instance, :code:`dsco up --dev` 
consists of the command :code:`up` and the option :code:`--dev`. This 
would be processed by the subparser :code:`up` and would launch the 
command required to bring up a dev container.

This module adds the subparsers in the :code:`commands` directory to our 
argument parser. The name of the :code:`commands` directory is specified 
as :code:`cmd_dir`. 

Each module in cmd_dir is expected to define the following:

    cmd_name (str) 
        The name of the sub-command
    
----

    add_subparser (subparsers)
        This should take the subparsers object created in this file and 
        add a subparser to it. 
        :code:`subparsers` is mutable so it does not need to return anything.

        Args
            subparsers (argparse._SubParsersAction) 
                The subparser object to which all sub-commands will 
                be assigned. 

        Returns
            None

----

    add_dispatch(dispatcher)
        The dispatcher dictionary maps the command given at the command 
        line to a function to be executed. For instance when we run 
        :code:`dsco up --dev`, the dispatcher would contain a mapping: 

            up --> function that launches dev container via docker-compose

        More specifically, add_dispatch takes the dispatcher dict 
        created in this file and adds an entry corresponding to the 
        command name. The entry should be a function that takes the 
        :code:`args` and :code:`conf` objects created in application.py 
        and executes the desired action.

        Args
            dispatcher (dict) 
                Dictionary containing the mappings :code:`cmd --> run_cmd`. 
                The dictionary is mutated to add a new mapping. For 
                consistency, you should name the function 
                :code:`run_cmd`, but this is not required. 

                We will define the requirements on the mapping next:

                cmd (string)
                    This is the name of the subparser

                run_cmd(args, conf)
                    Function executing desired action.

                    Args
                        args (argParse.Namespace)
                            This contains the command line arguments as 
                            parsed by the appropriate subparser.

                        conf (dict)
                            This dictionary contains project specific 
                            settings such as the project root directory, 
                            settings from the pyproject.toml file 
                            (if it exists) etc.

                    Returns
                        None

----

    Example: See :py:mod:`dsco.commands`.

With this structure in place, this file first creates the objects:

    parser (argparse.ArgumentParser)
        Interpret command line options

    subparsers (argparse._SubParsersAction)
        Contains definitions of sub commands.

    dispatcher (dict)
        dictionary used to run command based on command line inputs.

Then for each module found in :code:`cmd_dir` (files of the form 
:code:`*.py`, excluding files that begin with :code:`"_"`) we add all 
the subparsers and dispatchers with:

    - module.add_subparser(subparsers)
    - module.add_dispatch(dispatcher)

At run time, the application imports parser to interpret the command 
line options and dispatcher to run the appropriate command.
"""

import argparse
import importlib
from pathlib import Path

# Create parser, subparsers, and dispatcher for use in application
parser = argparse.ArgumentParser(prog="dsco")
subparsers = parser.add_subparsers(dest="cmd", help="available functionality")
dispatcher = dict()

# commands directory
cmd_dir = "commands"
cmd_path = Path(__file__).resolve().parent / cmd_dir

# create a list of all modules in cmd_dir unless they are private i.e. begin with "_"
is_not_hidden = lambda x: x[0] != "_"
file_list = sorted([p.stem for p in cmd_path.glob("*.py") if is_not_hidden(p.stem)])
module_list = [importlib.import_module(f"dsco.{cmd_dir}.{f}") for f in file_list]

# ======================================================================================
# add commands
#
for module in module_list:
    module.add_subparser(subparsers)
    module.add_dispatch(dispatcher)
