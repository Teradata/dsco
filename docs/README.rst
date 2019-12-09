
To configure container setup:

- If project is not local, create a docker-machine (for example sdl32267.labs.teradata.com): 
    ::

        docker-machine create \
            --driver generic \
            --generic-ip-address=sdl32267.labs.teradata.com \
            --generic-ssh-key "<path to key file>" \
            --generic-ssh-user=root sdl32267

- If project is not local, set environment to run commands on remote docker:
    ::

        eval "$(docker-machine env sdl32267)"

- Run VS Code in configured shell with 
    ::

        code .

- from VS Code attach to a container with: Remote Containers: Attach to Running Container...

- from VS Code command pallet run Remote-Containers: Open Attached Container Configuration File...
  ::

        {
            "extensions": [
                "bungcip.better-toml",
                "lextudio.restructuredtext",
                "ms-python.python"
            ],
            "shutdownAction": "none",
            "workspaceFolder": "/srv"
        }

- To unset environment:
    ::

        eval "$(docker-machine env -u)"

