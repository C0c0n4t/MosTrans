from flask import Flask
from flask_cors import CORS


application = Flask(__name__, template_folder="../frontend/templates", static_folder="../frontend/static")
application.config["SECRET_KEY"] = "MosTrans"


def run(port: int = 8080, host: str = "127.0.0.1"):
    """Runs application on 'http://{host}:{port}/'"""
    application.run(port=port, host=host)
