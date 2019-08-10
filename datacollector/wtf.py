# coding=utf-8

# 导入wtf扩展的表单类
from flask_wtf import FlaskForm
# 导入自定义表单需要的字段
from wtforms import SubmitField, StringField, PasswordField
# 导入wtf扩展提供的表单验证器
from wtforms.validators import DataRequired, EqualTo

# 自定义表单类，文本字段、密码字段、提交按钮
class Login(FlaskForm):
    id = StringField(label='工号', validators=[DataRequired('工号不能为空')])
    name = StringField(label='用户', validators=[DataRequired('用户名不能为空')])
    key = PasswordField(label='秘钥', validators=[DataRequired('秘钥不能为空'), EqualTo('key1', '秘钥不一致')])
    key1 = PasswordField(label='确认', validators=[DataRequired('秘钥不能为空')])
    submit = SubmitField('登录')

