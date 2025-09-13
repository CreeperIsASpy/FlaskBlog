from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
from sqlmodel import SQLModel, create_engine
from config import Config

def create_app():
    mail = Mail()

    # Initialize Flask app
    app = Flask(__name__)
    app.config.from_object(Config)
    mail.init_app(app)

    # Initialize Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    # Initialize database
    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])


    # 确保表在应用启动时被创建
    @app.before_first_request
    def create_tables():
        SQLModel.metadata.create_all(engine)


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
