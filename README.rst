==========================
DSCO (Draft documentation)
==========================
(D)ata (S)cience (Co)ntainer

A utility to create a data science development container.

Install
-------

::

    pip install git+https://github.td.teradata.com/Quality-Engineering/dsco.git

Features
--------

- Uses `poetry <https://poetry.eustace.io/>`_ to keep track of dependencies.
- Uses nginx and uwsgi to serve:

  - Jupyter (uwsgi)
  - Static reports (nginx)
  - Flask (uwsgi)

    - Dask

- Starts with a project skeleton that includes:

  - resources to build production and dev containers with docker / ansible.
  - flask skeleton already set up for use as api
  - dask skeleton integrated into flask for quickstart web dashboards

Commands
--------

dsco init
  Creates a new project directory

  example::

      dsco init

  Running this will prompt for project name and other information.

dsco go
  Launch container and open info page in a browser.
  First build should take approximately 7 minutes.
  After the image has been built, this command should finish almost instantly.

dsco build
  Build images only

dsco gen_reports
  Build the static html versions of reports created in the reports directory.

dsco restart_flask
  Restart flask in the container. Necessary to pick up changes made.

dsco rm
  Delete containers.

dsco rmi
  Delete containers and images.

dsco shell
  Open up a shell in a container.

dsco update_port
  Update to ports used for the containers.
