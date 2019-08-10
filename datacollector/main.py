# coding=utf-8

from flask import Flask, render_template, request, session, redirect, url_for, flash, make_response
from wtf import Login
from Config import Config
import common

config = Config("configs/config.json")

app = Flask(__name__)
app.secret_key = 'myprojectkey'



@app.route('/', methods=['get', 'post'])
def login():

    form = Login()
    if form.validate_on_submit():

        id = form.id.data
        name = form.name.data
        key = form.key.data

        # key1 = form.key1.data
        # print(id, name, key, key1)
        # return redirect(url_for('login_wtf'))

        common.print_info("id:%s, name:%s, key:%s is trying to login" % (id, name, key))

        # 如果是管理员
        if config.is_admin(id):
            if not name == config.get_admin_name(id):
                common.print_err("admin name err with id: %s, %s is not %s" % (id, key, config.get_admin_name(id)))
                flash("用户名错误")
                return redirect(url_for("login"))

            if not key == config.get_admin_key(id):
                common.print_err("admin key err with id: %s, %s is not %s" % (id, key, config.get_admin_key(id)))
                flash("秘钥错误")
                return redirect(url_for("login"))

            # 都正确，信息存入session、cookie
            # session['admin_id'] = id
            # session['admin_name'] = name
            # session['admin_key'] = key
            resp = make_response(render_template('admin.html', id=id, name=name))
            resp.set_cookie('id', id)
            resp.set_cookie('name', name)
            return resp

        # 如果是普通用户
        if config.is_user(id):
            if not name == config.get_user_name(id):
                common.print_warn("user name err with id: %s, %s is not %s" % (id, key, config.get_user_name(id)))
                flash("用户名错误")
                return redirect(url_for("login"))

            if not key == config.get_user_key(id):
                common.print_warn("user key err with id: %s, %s is not %s" % (id, key, config.get_user_key(id)))
                flash("秘钥错误")
                return redirect(url_for("login"))

            # 都正确，信息存入session、cookie
            resp = make_response(render_template('user.html', id=id, name=name))
            resp.set_cookie('id', id)
            resp.set_cookie('name', name)
            return resp
        else:
            flash('抱歉，用户%s并未获得授权，请联系%s' % (name, config.get_1st_admin_name()))
            return render_template('index.html', form=form)

    return render_template('index.html', form=form)



if __name__ == '__main__':
    app.run(debug=True)

