
from flask import Flask

def create_app():
    from . import index,api
    app  = Flask(__name__)
    app.register_blueprint(index.bp)
    app.register_blueprint(api.bp)
    return app


