from data.db_session import sessions

from backend.application import application
from flask import render_template


@application.route("/", methods=["GET"])
def index():
    """Website home page"""

    from data.models import Line, Station

    data = dict()
    data["lines"] = [line.name for line in sessions["train_database"].query(Line).order_by(Line.name).all()]
    data["stations"] = [station.name for station in sessions["train_database"].query(Station).order_by(Station.name).all()]
    return render_template("index.html", data=data)
