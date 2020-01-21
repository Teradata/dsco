"""Parse command line arguments
"""

import argparse
import importlib
from dsco.subparsers import (
    init,
    go,
    up,
    build,
    rm,
    rmi,
    shell,
    restart_flask,
    gen_reports,
    update_port,
    ls,
    code,
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
    up,
    build,
    rm,
    rmi,
    shell,
    restart_flask,
    gen_reports,
    update_port,
    ls,
    code,
]:
    module.add_cmd(subparsers)
    module.add_dispatch(dispatcher)
