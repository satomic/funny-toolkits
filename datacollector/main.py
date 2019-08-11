# coding=utf-8

from flask import Flask, render_template, request, session, redirect, url_for, flash, make_response
from wtf import Login,KeyGen,UpdateData
from Config import Config
import common.common as common
import common.hash_utils as hash_utils




app = Flask(__name__)
app.secret_key = 'myprojectkey'

db_file = "database.db3"
config = Config("configs/config.json", db_file=db_file)

@app.route('/', methods=['get', 'post'])
def login():

    form_login = Login()
    form_genkey = KeyGen()
    form_update_data = UpdateData()

    if form_login.validate_on_submit():

        id = form_login.id.data
        name = form_login.name.data
        key = form_login.key.data

        # key1 = form.key1.data
        # print(id, name, key, key1)
        # return redirect(url_for('login_wtf'))

        common.print_info("id:%s, name:%s, key:%s is trying to login" % (id, name, key))

        # 如果是管理员
        if config.is_admin(id):
            if not name == config.get_admin_name_by_id(id):
                common.print_err("admin name err with id: %s, %s is not %s" % (id, key, config.get_admin_name(id)))
                flash("用户名错误")
                return redirect(url_for("login"))

            if not key == config.get_admin_key_by_id(id):
                common.print_err("admin key err with id: %s, %s is not %s" % (id, key, config.get_admin_key(id)))
                flash("秘钥错误")
                return redirect(url_for("login"))

            # 都正确，信息存入session、cookie
            # session['admin_id'] = id
            # session['admin_name'] = name
            # session['admin_key'] = key
            resp = make_response(render_template('admin.html', id=id, name=name, form=form_genkey))
            resp.set_cookie('id', id)
            resp.set_cookie('name', name)
            return resp

        # 如果是普通用户
        if config.is_user(id):
            wanted_name = config.get_user_name_by_id(id)
            if not name == config.get_user_name_by_id(id):
                common.print_warn("user name err with id: %s, %s is not wanted value: %s" % (id, name, wanted_name))
                flash("用户名错误")
                return redirect(url_for("login"))

            key_realtime = hash_utils.hash(id, name)
            if not key == key_realtime:
                common.print_warn("user key err with id: %s, %s is not wanted value: %s" % (id, key, key_realtime))
                flash("秘钥错误")
                return redirect(url_for("login"))

            # 都正确，信息存入session、cookie
            resp = make_response(render_template('user.html', id=id, name=name, form=form_update_data))
            resp.set_cookie('id', id)
            resp.set_cookie('name', name)
            common.print_info("set id:%s, name:%s to cookies" % (id, name))
            return resp
        else:
            flash('抱歉，用户%s并未获得授权，请联系%s' % (name, config.get_1st_admin_name()))
            return render_template('index.html', form=form_login)

    return render_template('index.html', form=form_login)

@app.route('/admin', methods=['get', 'post'])
def admin():
    form_keygen = KeyGen()
    if form_keygen.validate_on_submit():
        id_new = form_keygen.id_new.data
        name_new = form_keygen.name_new.data
        key_new = hash_utils.hash(id_new, name_new)
        common.print_info("id: %s, name: %s, key: %s" % (id_new, name_new, key_new))

        # 保存到数据库
        config.update_user(id_new,name_new,key_new)

        # 获取cookie中的值，已登录用户
        id = request.cookies.get('id')
        name = request.cookies.get('name')

        flash("生成的秘钥为：%s，请牢记此秘钥" % key_new)
        return render_template('admin.html', id=id, name=name, id_new=id_new, name_new=name_new, form=form_keygen)
    return render_template('admin.html', form=form_keygen)

@app.route('/user', methods=['get', 'post'])
def user():
    form_update_data = UpdateData()
    if form_update_data.validate_on_submit():
        city = form_update_data.city.data
        project = form_update_data.project.data
        value = form_update_data.value.data
        common.print_info("city: %s, project: %s, value: %s" % (city, project, value))

        # 获取cookie中的值，已登录用户
        id = request.cookies.get('id')
        name = request.cookies.get('name')
        common.print_info("get id:%s, name:%s from cookies" % (id, name))
        return render_template('user.html', id=id, name=name, form=form_update_data)
    return render_template('user.html', form=form_update_data)


if __name__ == '__main__':
    app.run(debug=True)

