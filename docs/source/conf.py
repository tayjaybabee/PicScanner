# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import os
import sys
sys.path.insert(0, os.path.abspath('../../pic_scanner'))


project = 'PicScanner'
copyright = '2024, Inspyre-Softworks'
author = 'Inspyre-Softworks'
release = '1.0.0-dev.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
        'sphinx.ext.autodoc',
        'sphinx.ext.napoleon',
        'sphinx.ext.viewcode',
        'sphinx_rtd_theme',
        'sphinx.ext.autosummary',
        'sphinx.ext.autosectionlabel',
        'sphinx.ext.inheritance_diagram',
        'sphinx.ext.ifconfig',
        'sphinx_autodoc_typehints',
        'autoapi.extension',
        ]

templates_path = ['_templates']

autodoc_default_options = {
    'members': True,
    'undoc-members': True,
    'private-members': True,
    'special-members': '__init__',
    'inherited-members': True,
    'show-inheritance': True,
    'class-doc-from': 'class'
}

autodoc_member_order = 'alphabetical'


autoapi_dirs = ['../../pic_scanner']
autoapi_type = 'python'
autoapi_options = [
        'members',
        'undoc-members',
        'show-inheritance',
        'show-module-summary',
        'imported-members'
        ]

autodoc_typehints = 'both'


exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
