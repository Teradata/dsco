.. .. image:: ../assets/space-shuttle-launch.png

.. image:: ../assets/banner.png

Overview
=========

Why :code:`dsco`?

Dsco takes an opinionated view of a typical data science workflow 
and wraps all the necessary tools 
into a container that can be run locally, on a remote VM, 
or on kubernetes.

A typical project starts in a Jupyter notebook with some exploratory 
analysis.

    Dsco runs a jupyter notebook server.

Jupyter notebooks are great, but can be hard to share with other people.
There are some great tools to convert the notebooks into a static 
format, but they always requires a bit of time to figure it 
out again and get everything set up. Then of course we need 
to figure out how we send people the output.
If we're running in a container, can't we just park it on a VM 
somewhere and send them a link? Yes!

    Dsco generates and serves static html representations of your notebooks

Uh oh, did I loose a few of you? Set up a VM? Not me! Don't worry, I 
have a solution for you too. Just configure your github repo to use 
github pages and serve content out of your master branch docs folder 
`(don't worry, it's not hard) <https://help.github.com/en/github/working-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site>`_.

    Dsco generates static html representations of your notebooks that are compatible with github pages

Sounds pretty good, you say, but what if I need to add different python 
dependencies? No problem.

    Dsco gives you the tools to manage your python dependencies. No limits.

If all this sounds useful, then :code:`dsco` is for you! Head over to 
the :doc:`quickstart` to get going.

If you're still not convinced, I have some good news: 
:doc:`there's more! <features>`


Contents
================================

.. toctree::
   :maxdepth: 4

   Github <http://github.com/Teradata/dsco>
   quickstart
   features
   commands
   developer
   roadmap


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
