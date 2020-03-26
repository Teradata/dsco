.. image:: docs/assets/banner.png

==========================
DSCO
==========================

A utility to create a data science development container.

Documentation
-------------

`github pages <https://teradata.github.io/dsco/html/>`_


Features
--------

DSCO creates a development container that:

  - runs a jupyter notebook server.
  - generates static html representations of your notebooks 
    for easy sharing with anyone by either the included server
    or github pages.
  - manages python dependencies with `poetry <https://python-poetry.org/>`_.
  - integrates with vscode for an IDE with a local-like feel.

If that's not enough, you also get:

  - `Flask <https://palletsprojects.com/p/flask/>`_ and 
    `plotly | Dash <https://dash.plotly.com/>`_ for creating dashboards 
    and REST APIs.
  - Sphinx for automatic code documentation.
  - Useful Jupyter extensions installed and configured.
  - Your local project directory mounted and synced.
  - Ansible playbooks that build everything from scratch.

Install
-------

::

    pip install git+ssh://git@github.com/Teradata/dsco.git

Ultra Quickstart
----------------

See also: `Quickstart <https://teradata.github.io/dsco/html/quickstart.html>`_

Create project :code:`foo` in the current directory:

::

    >>> dsco init
    Using template: ...
    Creating project in ...
    project_name [MyProject]: foo
    author [Discovery]: 
    version [0.1]: 
    year [2020]: 
    project_port [8001]:

Build the development image and create a development container:

::

    >>> cd foo
    >>> dsco go
    docker-compose up -d dev
    Building dev
    ...
    <lots of ansible output>
    ...
    Creating foo_dev_1 ... done
    ========================================================================================
    execution time: 490.9753198623657 seconds
    ========================================================================================
