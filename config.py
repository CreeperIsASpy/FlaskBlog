import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('POSTGRES_URL')  # postgres_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    json_encoders = {"keys": ""}

    MAIL_SERVER = 'smtp.example.com'  # 邮件服务器
    MAIL_PORT = 587  # 邮件服务器端口
    MAIL_USE_TLS = True  # 使用 TLS
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')  # 邮件用户名
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')  # 邮件密码
    MAIL_DEFAULT_SENDER = 'blogging@creeperspy.com'  # 默认发件人
