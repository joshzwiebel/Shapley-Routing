# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys
sys.path.insert(0, os.path.abspath('../../'))

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'shapleyrouting'
copyright = '2023, Connor Sweet, Josh Zwiebel, Zahin Zaman'
author = 'Connor Sweet, Josh Zwiebel, Zahin Zaman'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.napoleon',
]

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'pydata_sphinx_theme'
html_static_path = ['_static']

# preserve default argument values as in source code
autodoc_preserve_defaults = True


# html_logo = '../img/logo.png'

html_theme_options = {
    'icon_links': [
        {
            'name': 'GitHub',
            'url': 'https://github.com/joshzwiebel/Shapley-Routing',
            'icon': 'fab fa-github-square',
            'type': 'fontawesome',
        },
    ],
    'external_links': [
        # {
        #     'name': 'Some external url name',
        #     'url': 'https://www.google.com/',
        # },
    ],
    'show_nav_level': 1,
    'navigation_depth': 2,
    'collapse_navigation': False,
    'show_prev_next': True,
    'use_edit_page_button': False,
}
