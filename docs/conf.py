import sys
import os

sys.path.append(os.path.abspath('..'))
project = 'hw_fastapi'
copyright = '2023, sergii'
author = 'sergii'

extensions = ['sphinx.ext.autodoc']

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

html_theme = 'nature'
html_static_path = ['_static']
