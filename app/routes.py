from flask import Blueprint, render_template, request, url_for, flash
from flask_login import login_required, current_user
from sqlmodel import Session, select
from werkzeug.utils import redirect

from app import engine
from app.models import Post, User

# 创建蓝图
main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/dashboard')
@login_required
def dashboard():
    with Session(engine) as session:
        user = session.exec(
            select(User).where(User.id == current_user.id)
        ).first()
        if user:

            # 显式加载 posts 关系
            session.refresh(user)
            posts = user.posts if hasattr(user, "posts") else []
        else:
            posts = []
        return render_template('dashboard.html', name=current_user.username, posts=posts)


@main.route('/create_post', methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')

        if not title or not content:
            flash('Title and content are required!')
        else:
            new_post = Post(title=title, content=content, author_id=current_user.id)
            with Session(engine) as session:
                session.add(new_post)
                session.commit()
                print(f"New post created: {new_post}")  # 调试信息
                flash('Your post has been created!')
            return redirect(url_for('main.dashboard'))

    return render_template('create_post.html')


@main.route('/post/<int:post_id>')
def view_post(post_id):
    with Session(engine) as session:
        post = session.get(Post, post_id)
        if post:
            return render_template('view_post.html', post=post)
        else:
            flash('Post not found!')
            return redirect(url_for('main.index'))


@main.route('/edit_post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    with Session(engine) as session:
        post = session.get(Post, post_id)
        if not post:
            flash('Post not found!')
            return redirect(url_for('main.dashboard'))
        if post.author_id != current_user.id:
            flash('You do not have permission to edit this post!')
            return redirect(url_for('main.dashboard'))

        if request.method == 'POST':
            title = request.form.get('title')
            content = request.form.get('content')

            if not title or not content:
                flash('Title and content are required!')
            else:
                post.title = title
                post.content = content
                session.commit()
                flash('Your post has been updated!')
                return redirect(url_for('main.view_post', post_id=post.id))

        return render_template('edit_post.html', post=post)


@main.route('/delete_post/<int:post_id>', methods=['POST'])
@login_required
def delete_post(post_id):
    with Session(engine) as session:
        post = session.get(Post, post_id)
        if not post:
            flash('Post not found!')
            return redirect(url_for('main.dashboard'))
        if post.author_id != current_user.id:
            flash('You do not have permission to delete this post!')
            return redirect(url_for('main.dashboard'))

        session.delete(post)
        session.commit()
        flash('Your post has been deleted!')
        return redirect(url_for('main.dashboard'))
