from pathlib import Path
from distutils.dir_util import copy_tree


# Project directories
project_dir = Path(".")
cache_dir = project_dir / "builder" / "cache"
project_certs_dir = cache_dir / "ca-certificates"

# Configuration directories
dsco_config_dir = Path.home() / ".dsco"
user_certs_dir = dsco_config_dir / "ca-certificates"

# copy user certs into cache dir
if user_certs_dir.exists():
    copy_tree(
        str(user_certs_dir.resolve()), str(project_certs_dir.resolve())
    )
