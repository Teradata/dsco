import jinja2
from jinja2 import meta
import os
from types import SimpleNamespace
import inspect

############################
# set up jinja environment #
############################
FILENAME = inspect.getframeinfo(inspect.currentframe()).filename
CURRENT_DIR = os.path.dirname(os.path.abspath(FILENAME))
SQL_DIR_PATH = os.path.join(CURRENT_DIR, "sql")
# create search path that includes all subdirectories of SQL_DIR_PATH
sql_search_path = [directory for (directory, _, _) in os.walk(SQL_DIR_PATH)]

# define template loader
loader = jinja2.FileSystemLoader(searchpath=sql_search_path)

# create environment
env = jinja2.Environment(loader=loader)

sql = SimpleNamespace()

sql.all_test_queries = env.get_template("all_test_queries.sql")
sql.events = env.get_template("events.sql")

