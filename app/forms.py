from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired


class CommentForm(FlaskForm):
    content = TextAreaField('评论内容', validators=[DataRequired()])
    submit = SubmitField('提交评论')


class EditCommentForm(FlaskForm):
    content = TextAreaField('评论内容', validators=[DataRequired()])
    submit = SubmitField('更新评论')
