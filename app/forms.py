from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired


class PostForm(FlaskForm):
    title = StringField('标题', validators=[DataRequired()])
    content = TextAreaField('内容', validators=[DataRequired()])
    submit = SubmitField('发布')


class CommentForm(FlaskForm):
    content = TextAreaField('评论内容', validators=[DataRequired()])
    submit = SubmitField('提交评论')


class EditCommentForm(FlaskForm):
    content = TextAreaField('评论内容', validators=[DataRequired()])
    submit = SubmitField('更新评论')
