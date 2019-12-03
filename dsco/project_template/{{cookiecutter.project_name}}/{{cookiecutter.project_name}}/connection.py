import teradataml as td
import configparser
from sqlalchemy.exc import OperationalError, StatementError
from definitions import CONNECTION_FILE

default_file = CONNECTION_FILE
default_section = "default_connection"
num_retries = 3


def connected():
    """Check status of connection"""
    try:
        td.get_connection().execute("select 1;")
    except (AttributeError, OperationalError, StatementError):
        return False
    else:
        return True


def parse_options(file_name=None, section="default_connection", **kwargs):
    # we need at least one but not both ...
    if file_name and kwargs:
        raise ConnectionError("Connect with file or arguments")
    elif not file_name and not kwargs:
        raise ConnectionError("Must provide connection file or arguments")

    # set options based on what was provided
    if file_name:
        return parse_file(file_name=file_name, section_name=section)
    else:
        return kwargs


def parse_file(file_name=default_file, section_name=default_section):
    """Parse ini connection file"""
    if connected():
        td.remove_context()

    config = configparser.ConfigParser()

    config.read(file_name)

    if section_name.lower() == "default_connection":
        section = config[config["default_connection"]["section"]]
    else:
        section = config[section]

    return dict(section.items())


def connect_with_file(file_name=default_file, section=default_section):
    """Connect with parameters from file"""
    d = parse_file(file_name=file_name, section_name=section)
    connect(**d)


def connect(**kwargs):
    """Create connection"""
    if connected():
        td.remove_context()

    try:
        td.create_context(**kwargs)
    except:
        # print(e)
        # something failed, try again
        td.create_context(**kwargs)


class ConnectionManager(object):
    """Tools to safely use a connection"""

    def __init__(self):
        self.options = None

    def set_connection(self, file_name=None, section=default_section, **kwargs):
        self.options = parse_options(file_name=file_name, section=section, **kwargs)

    def connect(self):
        connect(**self.options)

    def execute(self, query):
        for _ in range(num_retries):
            try:
                return td.get_connection().execute(query)
            except (AttributeError, OperationalError, StatementError):
                if connected():
                    # we're connected so something was wrong with the query
                    break
                else:
                    self.connect()
        # we were unable to run the query

    def connected(self):
        return connected()

    def get_connection(self):
        return td.get_connection()

    def get_context(self):
        return td.get_context()

    def from_query(self, *args, **kwargs):
        if not self.connected():
            self.connect()
        return td.DataFrame.from_query(*args, **kwargs)

    def from_table(self, *args, **kwargs):
        if not self.connected():
            self.connect()
        return td.DataFrame.from_table(*args, **kwargs)


db = ConnectionManager()
