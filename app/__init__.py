import click
from flask import Flask
from flask_login import LoginManager
from sqlmodel import SQLModel
from config import Config


def init_db():
    """A function to create database tables."""
    # Import the engine here to avoid circular dependency issues
    from app.models import init_db_engine, engine
    SQLModel.metadata.create_all(engine)


# This creates a new command that you can run from your terminal
# To run it, you'll type: flask init-db
@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


def create_app():
    # Initialize Flask app
    app = Flask(__name__)
    app.config.from_object(Config)
    app.cli.add_command(init_db_command)

    # Initialize Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    from app.models import init_db_engine

    init_db_engine(app.config['SQLALCHEMY_DATABASE_URI'])

    @login_manager.user_loader
    def load_user(user_id):
        from app.models import User  # 延迟导入以避免循环依赖
        from sqlmodel import Session
        with Session(engine) as session:
            return session.get(User, int(user_id))

    # 延迟导入路由和模型
    from app import routes, models, auth

    # 注册蓝图
    app.register_blueprint(routes.main)
    app.register_blueprint(auth.auth)

    # 注册错误处理
    app.register_error_handler(404, routes.page_not_found)
    app.register_error_handler(500, routes.internal_server_error)

    return app
