# coding=utf-8

from flask import Flask, render_template, request, session, redirect, url_for, flash
from Config import Config

config = Config("configs/config.json")

app = Flask(__name__)
app.secret_key = 'myprojectkey'

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['get', 'post'])
def login():

    id = request.form.get('id')
    name = request.form.get('name')
    key = request.form.get('key')

    # 如果是管理员
    if config.is_admin(id):
        if not name == config.get_admin_name(id):
            flash("管理员用户名错误")
            return render_template(url_for("login"))

        session['admin_id'] = id
        session['admin_name'] = name
        session['admin_key'] = key
        return render_template('admin.html', name=session.get('admin_name'), id=session.get('admin_id'))

    # 如果是普通用户
    if config.is_user(id):
        flash('抱歉，用户%s并未获得授权，请联系%s' % (name, config.get_admin_name()))
    return render_template('login.html', name=session.get('name'))

if __name__ == '__main__':
    app.run(debug=True)

