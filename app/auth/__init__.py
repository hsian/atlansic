from flask import Blueprint
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
 
auth = Blueprint('auth', __name__)
TokenAuth = HTTPTokenAuth() 

from . import api
