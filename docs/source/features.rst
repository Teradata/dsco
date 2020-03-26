=========
Features
=========

jupyter server
--------------

The is a jupyter notebook server running in the container.


dependency management
---------------------

We use poetry to manage dependencies


convert notebooks to static html
--------------------------------

We can convert source content written in reStructuredText files or 
jupyter notebook files to static html. The resulting output 
can be accessed from a web server running in the container or 
from github pages.


connect to your container with vscode (local or remote)
-------------------------------------------------------

We can use vscode running locally to connect to running 
container on our localhost or on a remote host. This gives 
the same feel as developing in a local IDE. 

Dsco is tooled around using vscode, but does not preclude the use 
of other IDEs if you can make them work. For me, this project 
was the impetus for switching from PyCharm to VsCode and 
I have not been disappointed.


create a dashboard in plotly | Dash
-----------------------------------

plotly | Dash is running within Flask and there is a bare bones 
project up and running at startup. It's pretty straight forward 
to expand from here without having to do a lot of the plumbing 
work up front.

One workflow that works well is to develop the plotly plot in 
your jupyter notebook (plotly renders nicely in static html by 
the way, keeping it's interactivity), then when you're ready 
to create your dashboard, pull the code into your package 
directory and use it in Dash!


create a rest api
-----------------

Since Flask is already running, you can easily set up new routes 
to create rest APIs. This means you can use this container as 
the basis for data science micro-services. Handle the data 
processing in one and the dashboard in another. 


auto document your code
-----------------------

Use sphinx to automatically generate documentation for your code. 
This includes both project documentation and reports, or what I 
generally think of as EDA.


jupyter extensions
------------------

A selection of jupyter extensions is already configured. 
This includes:

    - Table of contents
    - Ruler
    - Spell checking on markdown cells


build from scratch
------------------

The entire recipe for you project is contained in your project 
directory. Once created, dsco facilitates working with your 
project, but is not required. This means someone else can 
pull your project from git and build everything needed to run 
your project locally, or on a vm. All that's really required is 
Docker. 

Generally, dsco is just a wrapper of docker commands. 
When running dsco commands, the equivalent docker command is 
also shown.

The dsco workflow has been used successfully on mac, linux, 
and windows (under the new wsl2, expected to be generally 
available in Windows 10, version 2004 sometime in April 2020).


local project directory mounted inside container
------------------------------------------------

When working in the dev container, your project folder is 
mounted into the container at :code:`/srv`. This means you 
can run git commands from your local machine without 
having to worry about getting your git credentials 
installed in your container and potentially checking 
those into git! oops (-_-). It also means that if you 
accidentally delete your container, you work is still 
on your hard drive.

Unlike the dev container, the project directory is 
copied into the prod container. 