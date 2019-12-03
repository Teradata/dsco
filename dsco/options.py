"""Parse command line arguments
"""

import argparse
import importlib
from dsco.subparsers import (
    init,
    go,
    build,
    rm,
    rmi,
    shell,
    restart_flask,
    gen_reports,
    update_port,
)


parser = argparse.ArgumentParser(prog="dsco")
subparsers = parser.add_subparsers(dest="cmd", help="available functionality")

dispatcher = dict()

# ======================================================================================
# add commands (subparsers)
#
for module in [
    init,
    go,
    build,
    rm,
    rmi,
    shell,
    restart_flask,
    gen_reports,
    update_port,
]:
    module.add_cmd(subparsers)
    module.add_dispatch(dispatcher)
