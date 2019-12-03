#!/usr/bin/env python
# * encoding: utf-8
import os


def _test_dir(dir_path):
    if not os.path.isdir(dir_path):
        raise IOError(f"Expected specs directory at {dir_path}")


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


SQL_DIR = os.path.join(ROOT_DIR, "{{ cookiecutter.project_name }}", "sql")
_test_dir(SQL_DIR)
