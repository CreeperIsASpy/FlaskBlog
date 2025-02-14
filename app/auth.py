from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from sqlmodel import Session
from app.models import User
from app import engine  # 导入 engine

# 创建蓝图
auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        with Session(engine) as session:
            user = session.query(User).filter(User.username == username).first()

            if user and check_password_hash(user.password_hash, password):
                login_user(user)  # 登录用户
                return redirect(url_for('main.dashboard'))
            else:
                flash('用户名或密码错误！')
    return render_template('login.html')


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        hashed_password = generate_password_hash(password, method='sha256')

        new_user = User(username=username, email=email, password_hash=hashed_password)
        with Session(engine) as session:
            session.add(new_user)
            session.commit()

        return redirect(url_for('auth.login'))
    return render_template('register.html')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('你已登出！')
    return redirect(url_for('main.index'))
