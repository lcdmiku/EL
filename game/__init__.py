#game\__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()


def init_app(app):
    db.init_app(app)
    migrate.init_app(app, db)

def create_app(config_class='config.Config'):
    app = Flask(__name__, static_folder='static')
    app.config.from_object(config_class)
    # 调用 init_app 函数来初始化 SQLAlchemy 和 Flask-Migrate
    init_app(app)

    from .models.user import User
    from .models.NPC import NPC
    #create all the tables
    with app.app_context():
        db.create_all()

    # 延迟导入蓝图以避免循环导入
    def register_blueprints():
        from .routes.login import login_bp
        from .routes.play import play_bp

        app.register_blueprint(login_bp)
        app.register_blueprint(play_bp)

    register_blueprints()

    return app