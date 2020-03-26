"""Create subparsers

See the :py:mod:`dsco.options` module to find an explanation of 
how the subparsers defined here are added to the main parser.

Each module defined here is expected to declare the following:

    cmd_name(str)
        The name of the sub-command
    
----

    add_subparser(subparsers)
        Args:
            subparsers (argparse._SubParsersAction)
                The subparser object to which all sub-commands will 
                be assigned. 

        Returns:
            None

----

    add_dispatch(dispatcher)
        Args:
            dispatcher (dict)
                Dictionary mapping :code:`cmd --> run_cmd`.

                cmd (string)
                    This is the name of the subparser

                run_cmd(args, conf)
                    Executes the desired action.

                    Args
                        args (argParse.Namespace)
                            This contains the command line arguments as 
                            parsed by the appropriate subparser.

                        conf (dict)
                            This dictionary contains project 
                            specific settings such as the project root 
                            directory, settings from the pyproject.toml 
                            file (if it exists) etc.

                    Returns
                        None

Example:
    Let's look at a simple example. Say we wanted to create a subparser 
    called :code:`project_info` such that when we run the command 
    :code:`dsco project_info` we get the directory name of the project 
    root directory, or :code:`None` if we were not in a project 
    directory tree. We also want to be able to add a :code:`-v`, or 
    :code:`--verbose` option to get the information in 
    the :code:`pyproject` file.

    We would create a file called :code:`project_info.py` and it would 
    contain the following:

    .. code-block:: python

        # Assign the file name without extension to cmd_name.
        # Naming the command in this way ensures the file name 
        # and command name stay in sync.
        from pathlib import Path
        cmd_name = Path(__file__).stem

        def add_subparser(subparsers):
            # create the basic command
            sub = subparsers.add_parser(
                cmd_name, help="list the project root dir"
            )
            # add the -v option
            sub.add_argument(
                "-v", 
                "--verbose", 
                action="store_true", 
                help="Also show information in pyproject file",
            )

        def run_cmd(args, conf):
            # Only return a value if dsco is run within a project tree
            # conf["proj_root"] is defined in application.py
            if conf["proj_root"]:
                print(conf["proj_root"])

                if args.verbose:
                    print(conf["pyproject"])
            else:
                print("None")

        
        def add_dispatch(dispatcher):
            dispatcher[cmd_name] = run_cmd
"""
