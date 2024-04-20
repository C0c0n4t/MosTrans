from backend.global_declarations import *

from backend.application import application
from flask import render_template


@application.route('/', methods=["GET"])
def base():
    """Website home page"""
    return render_template("base.html")
