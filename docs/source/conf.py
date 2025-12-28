import os
import sys

sys.path.insert(0, os.path.abspath('../../'))

project = 'HM11 REST API'
author = 'Artem'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon'
]

html_theme = 'alabaster'
