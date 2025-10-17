# Configuration file for the Sphinx documentation builder.
import os
import sys

# -- Path setup --------------------------------------------------------------
# Point Sphinx to the source code so it can find the docstrings.
sys.path.insert(0, os.path.abspath('../../src'))


# -- Project information -----------------------------------------------------
project = 'AM215 Quality Demo'
copyright = '2024, The AM215 Team'
author = 'The AM215 Team'


# -- General configuration ---------------------------------------------------
# Add any Sphinx extension module names here, as strings.
extensions = [
    "sphinx.ext.autodoc",       # Automatically generate docs from docstrings
    "sphinx.ext.napoleon",      # Understand NumPy and Google style docstrings
    "sphinx_autodoc_typehints", # Render type hints in the documentation
]

templates_path = ['_templates']
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------
html_theme = 'alabaster'
html_static_path = ['_static']
