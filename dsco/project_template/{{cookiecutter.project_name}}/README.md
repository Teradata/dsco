# Datascience Development Environment
Date: May 28, 2019

## TL;DR
This is a cookiecutter template to create a datascience working environemnt within
a container. Launch the container with `./bin/dscogo` from the project root directory.

## **Key Features**

### Jupyter
When launched, the container will run a jupyter notebook. To access the notebook
go to `http://localhost:{{cookiecutter.project_port}}` and follow the instructions given there.

### Sphinx / nbsphinx
Use in reports and docs
command: `make html` from within the container or `./build_html` from within 
your project directory.

### Flask webapp

### Dockerfile

### Cache

### Docker-compose file

### Poetry

### Tests

### Commands
- start: see above
- build_html: see above
- dshell: access a shell within the container

## ToDo
- Improve documentation

## Notes
- supervisor can have problems running on an overlay FS in docker. Had to change
  socket file location in supervisor.conf to /dev/shm to fix.
- how to setup nginx/uwsgi/flask: https://flask.palletsprojects.com/en/1.1.x/deploying/uwsgi/#starting-your-app-with-uwsgi
- to use docker-machine to connect to a remote docker server: 
  ```
  docker-machine create \
    --driver generic \
    --generic-ip-address=sdl32267.labs.teradata.com \
    --generic-ssh-key "/Users/ap186098/.ssh/wla_deploy" \
    --generic-ssh-user=root sdl32267
  ```
- to set environment variables:
  ```
  eval "$(docker-machine env sdl32267)"
  ```
- to unset environment variables:
  ```
  eval "$(docker-machine env -u)"
  ```
