# Configuration file for the Sphinx documentation builder.

import os
import sys
docs_dir = os.path.abspath(os.path.dirname(__file__))
src_dir = os.path.join(docs_dir, '../../')
sys.path.insert(0, src_dir)

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Essence Extractor'
copyright = '2023, Jurik-001'
author = 'Jurik-001'
release = '0.0.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
        'sphinx.ext.autodoc',
        'sphinx_rtd_theme',
        'sphinx.ext.napoleon',
        'myst_parser',
]

templates_path = ['_templates']
exclude_patterns = []

# Napoleon settings
napoleon_google_docstring = True
napoleon_include_special_with_doc = True

# MyST settings
myst_heading_anchors: 2
myst_highlight_code_blocks: True


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
