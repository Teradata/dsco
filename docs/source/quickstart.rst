.. image:: ../assets/space-shuttle-launch.png

==========================
Quickstart
==========================

Install
-------

    :code:`pip install git+ssh://git@github.com/Teradata/dsco.git`

Start a project
---------------

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
    select python_version:
    1 - 3.7
    2 - 3.6
    Choose from 1, 2 [1]:

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

If you are running on your local machine, your project landing
page should have opened up in your browser. Sometimes the browser 
opens faster than the internal server starts so don't be alarmed if 
it takes a couple of seconds to load.

You can see what containers are running with:

::

    >>> dsco ls
    localhost
    NAME             LINK                    ID             STATUS                        SIZE
    foo_dev:latest                           4903b3c62ae2   7 minutes ago                 1.75GB
        foo_dev_1    http://localhost:8001   aa864a674b4f   Up 7 minutes

In most terminals, you should be able to click (or shift+click) on the 
link as another way to open the landing page.

Install dependencies
--------------------
We will be using `poetry <https://python-poetry.org/>`_ as our package 
manager. Dsco can be run without ever installing python locally, 
everything is **in** your container, so the easiest way to manage 
packages is to open a shell in your container:

::

    >>> # make sure you're still in your project directory
    >>> dsco shell
    docker exec -it $(docker ps --all --filter 'label=com.docker.compose.project=foo' --filter 'label=com.docker.compose.service=dev' --format {{.Names}}) bash -c 'cd /srv && exec "${SHELL:-sh}"'
    root@aa864a674b4f:/srv#

This opens up a bash prompt inside our container. Our project directory 
is mounted at :code:`/srv`, which is our current directory.

To list the python packages installed:

::

    >>> poetry show
    ...
    ipython   7.13.0   IPython: Productive Interactive Computing
    ...
    jupyter   1.0.0    Jupyter metapackage. Install all the Jupyter components in one go.
    ...
    pandas    0.24.2   Powerful data structures for data analysis, time series, and statistics
    ...

I've only listed a few of the packages here.

If we want to install scikit-learn:

::

    >>> poetry add scikit-learn
    Skipping virtualenv creation, as specified in config file.
    Using version ^0.22.2 for scikit-learn

    Updating dependencies
    Resolving dependencies... (3.3s)

    Writing lock file


    Package operations: 3 installs, 1 update, 0 removals

      - Installing joblib (0.14.1)
      - Installing scipy (1.4.1)
      - Installing scikit-learn (0.22.2.post1)
      - Updating tdsqlmagic (0.18 -> 0.18 builder/cache/tdsqlmagic-0.18-py3-none-any.whl)

Create Jupyter notebooks
------------------------

Creating notebooks should be a familiar process. Go to the 
**Jupyter** section of your landing page. There will be a link to 
your server there:

    Access your `Jupyter notebook server. <http://localhost:8001/notebook>`_

If you're on your local computer and you entered 8001 as your project 
port, the above link will work as well.

The jupyter server loads in the root of your project directory. 
You can create notebooks wherever you want, but Dsco tools are 
configured to expect your notebooks to be in the 
:code:`docs/reports/source` directory. Go ahead and create a 
notebook called :code:`foo_notebook.ipynb` in this directory and 
fill in a few cells. Now save and quit the notebook.

Because we've mounted our project directory into our container, 
you will see this new notebook on your local computer as well.

Create static output
--------------------

To create a static html version of your new notebook, we need to 
open :code:`/srv/docs/reports/source/index.rst` (you can do this 
through the Jupyter server interface).

.. literalinclude:: ../../dsco/project_template/{{cookiecutter.project_name}}/docs/reports/source/index.rst
   :language: RST
   :emphasize-lines: 13

This is a `reStructuredText <https://www.sphinx-doc.org/en/master/usage/restructuredtext/index.html>`_ 
file if you want to learn more about the formatting, but all you need 
to do is to add the name of your notebook under the highlighted line 
and save the file.

Like so ...

.. code-block::
   :emphasize-lines: 2

    reports_template
    foo_notebook

Now, from **outside** the container, within the project directory run:

::

    >>> dsco reports --generate
    docker exec -it $(docker ps --all --filter 'label=com.docker.compose.project=foo' --filter 'label=com.docker.compose.service=dev' --format {{.Names}}) bash -c 'cd /srv/docs/reports/source && make html'
    Running Sphinx v2.4.4
    ...
    build succeeded, 1 warning.

    The HTML pages are in ../html.

Now go back to your project landing page and follow the link in 
the Sphinx section to your reports section.

    Access static `reports <http://localhost:8001/reports/>`_ built from your notebooks

Again, if you're on your local computer and you entered 8001 as your project 
port, the above link will work as well.

QED
