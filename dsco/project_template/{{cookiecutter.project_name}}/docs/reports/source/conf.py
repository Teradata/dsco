# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# http://www.sphinx-doc.org/en/master/config

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))

import guzzle_sphinx_theme

# -- Project information -----------------------------------------------------

project = '{{ cookiecutter.project_name }}'
copyright = '{{ cookiecutter.year }}, {{ cookiecutter.author }}'
author = '{{ cookiecutter.author }}'

# The full version, including alpha/beta/rc tags
release = '{{ cookiecutter.version }}'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'nbsphinx',
    #'sphinxjp.themes.basicstrap',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store', '**.ipynb_checkpoints']


# -- Options for HTML output -------------------------------------------------
html_title = project + ' version ' + release
# Adds an HTML table visitor to apply Bootstrap table classes
html_translator_class = 'guzzle_sphinx_theme.HTMLTranslator'
html_theme_path = guzzle_sphinx_theme.html_theme_path()
html_theme = 'guzzle_sphinx_theme'

# Register the theme as an extension to generate a sitemap.xml
extensions.append('guzzle_sphinx_theme')

html_theme_options = {
    'project_nav_name': project,
    #'max-width': '1100px',
}
html_sidebars = {
    '**': ['logo-text.html', 'globaltoc.html', 'searchbox.html']
}

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
#html_theme = 'alabaster'
#html_theme = 'classic'
#html_theme = 'basicstrap'

#html_theme_options = {
#    'nav_fixed_top': True,
#    'nosidebar': True,
#    'content_fixed': True,
#    'content_width': '800px',
#}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

def setup(app):
    app.add_javascript('https://cdnjs.cloudflare.com/ajax/libs/require.js/2.1.10/require.min.js')
    #This next line causes errors: fixed the issued by placing plotly.js in _build/html directory
    #app.add_javascript('https://cdn.plot.ly/plotly-latest.min.js')
