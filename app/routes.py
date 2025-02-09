from flask import Blueprint, render_template, request, url_for, flash
from flask_login import login_required, current_user
from sqlmodel import Session, select, desc
from werkzeug.utils import redirect
from datetime import datetime

from app import engine
from app.models import Post, User, Comment
from app.forms import CommentForm, EditCommentForm

# 创建蓝图
main = Blueprint('main', __name__)


@main.route('/')
def index():
    with Session(engine) as session:
        # 查询最新的 10 篇博文，按创建时间倒序排列
        posts = session.exec(
            select(Post)
            .order_by(desc(Post.created_at))
            .limit(10)
        ).all()
        return render_template('index.html', posts=posts, datetime=datetime, len=len)


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
            flash('你必须填写标题和内容字段!')
        else:
            new_post = Post(title=title, content=content, author_id=current_user.id)
            with Session(engine) as session:
                session.add(new_post)
                session.commit()
                print(f"New post created: {new_post}")  # 调试信息
                flash('你成功创建了一篇新的博文!')
            return redirect(url_for('main.dashboard'))

    return render_template('create_post.html')


@main.route('/post/<int:post_id>')
def view_post(post_id):
    with Session(engine) as session:
        post = session.get(Post, post_id)
        if post:
            return render_template('view_post.html', post=post, form=CommentForm())
        else:
            flash('博文未找到！')
            return redirect(url_for('main.index'))


@main.route('/post/<int:post_id>/comment', methods=['POST'])
@login_required
def add_comment(post_id):
    form = CommentForm()
    if form.validate_on_submit():
        with Session(engine) as session:
            new_comment = Comment(
                content=form.content.data,
                author_id=current_user.id,
                post_id=post_id
            )
            session.add(new_comment)
            session.commit()
            flash('评论已发布！', 'success')
    return redirect(url_for('main.view_post', post_id=post_id))


@main.route('/edit_post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    with Session(engine) as session:
        post = session.get(Post, post_id)
        if not post:
            flash('博文未找到!')
            return redirect(url_for('main.dashboard'))
        if post.author_id != current_user.id:
            flash('你没有编辑这篇博文的权限!')
            return redirect(url_for('main.dashboard'))

        if request.method == 'POST':
            title = request.form.get('title')
            content = request.form.get('content')

            if not title or not content:
                flash('你必须填写标题和内容字段!')
            else:
                post.title = title
                post.content = content
                session.commit()
                flash('你的博文已被更新!')
                return redirect(url_for('main.view_post', post_id=post.id))

        return render_template('edit_post.html', post=post)


@main.route('/delete_post/<int:post_id>', methods=['POST'])
@login_required
def delete_post(post_id):
    with Session(engine) as session:
        post = session.get(Post, post_id)
        if not post:
            flash('博文未找到!')
            return redirect(url_for('main.dashboard'))
        if post.author_id != current_user.id:
            flash('你没有编辑这篇博文的权限!')
            return redirect(url_for('main.dashboard'))

        session.delete(post)
        session.commit()
        flash('你的博文已被删除!')
        return redirect(url_for('main.dashboard'))


@main.route('/comment/<int:comment_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_comment(comment_id):
    with Session(engine) as session:
        comment = session.get(Comment, comment_id)
        if not comment:
            flash('评论未找到！', 'error')
            return redirect(url_for('main.index'))
        if comment.author_id != current_user.id:
            flash('你没有权限编辑这条评论！', 'error')
            return redirect(url_for('main.view_post', post_id=comment.post_id))

        form = EditCommentForm()
        if form.validate_on_submit():
            comment.content = form.content.data
            session.commit()
            flash('评论已更新！', 'success')
            return redirect(url_for('main.view_post', post_id=comment.post_id))
        elif request.method == 'GET':
            form.content.data = comment.content

        return render_template('edit_comment.html', form=form, comment=comment)


# 删除评论
@main.route('/comment/<int:comment_id>/delete', methods=['POST'])
@login_required
def delete_comment(comment_id):
    with Session(engine) as session:
        comment = session.get(Comment, comment_id)
        if not comment:
            flash('评论未找到！', 'error')
            return redirect(url_for('main.index'))
        if comment.author_id != current_user.id:
            flash('你没有权限删除这条评论！', 'error')
            return redirect(url_for('main.view_post', post_id=comment.post_id))

        post_id = comment.post_id
        session.delete(comment)
        session.commit()
        flash('评论已删除！', 'success')
        return redirect(url_for('main.view_post', post_id=post_id))
