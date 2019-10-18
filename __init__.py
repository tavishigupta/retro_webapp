"""
The flask application package.
"""
from flask import Flask

# create flask app
app = Flask(__name__)
app.static_folder = 'static'

import Retro.retro