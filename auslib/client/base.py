from flask import Flask

from auslib.AUS import AUS3

app = Flask(__name__)
AUS = AUS3()

from auslib.client.views.client import *
