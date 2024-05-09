
from flask import Flask

def create_app():
    from . import index,api,apiv2
    app  = Flask(__name__)
    app.register_blueprint(index.bp)
    app.register_blueprint(api.bp)
    app.register_blueprint(apiv2.bp)

    return app


