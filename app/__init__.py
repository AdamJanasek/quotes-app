from flask import Flask

from app import controllers
from app.common.extensions import cache
from app.config import flask_config, flask_name


def create_app() -> Flask:
    app = Flask(flask_name, template_folder='templates', static_url_path='/static')
    app.config.from_object(flask_config)
    cache.init_app(app, config={'CACHE_TYPE': 'simple'})
    app.register_blueprint(controllers.bp, url_prefix='/')
    return app
