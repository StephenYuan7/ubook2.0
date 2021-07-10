from .app import Flask

from flask_cors import *


def register_blueprints(app):
    from app.api.v1 import create_blueprint_v1
    from app.api.v0 import create_blueprint_v0

    app.register_blueprint(create_blueprint_v1(), url_prefix='/v1')
    app.register_blueprint(create_blueprint_v0(), url_prefix='/v0')



# 注册数据库orm对象
def register_plugin(app):
    from app.models.base import db
    db.init_app(app)
    with app.app_context():
        db.create_all()


# 注册flask的核心对象
def create_app():
    # __name__为当前文件
    app = Flask(__name__)

    CORS(app, supports_credentials=True)

    # 导入两个配置文件
    app.config.from_object('app.config.setting')
    app.config.from_object('app.config.secure')

    register_blueprints(app)
    register_plugin(app)
    return app
