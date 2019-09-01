# coding=utf-8

import os
from flask import Flask, render_template, request, session, redirect, url_for, flash, make_response
from werkzeug.utils import secure_filename
from wtf import Login,KeyGen,UpdateData
from Config import Config
import common.common as common
import common.hash_utils as hash_utils
import common.file_utils as file_utils
from merge_data import excel_check,titles_std


UPLOAD_FOLDER = 'uploads'
app = Flask(__name__)
app.secret_key = 'myprojectkey'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

db_file = "data/database.db3"
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

    # 获取cookie中的值，已登录用户
    id = request.cookies.get('id')
    name = request.cookies.get('name')

    form_update_data = UpdateData()
    if form_update_data.validate_on_submit():
        common.print_info("提交表单数据")
        city = form_update_data.city.data
        project = form_update_data.project.data
        value = form_update_data.value.data
        common.print_info("city: %s, project: %s, value: %s" % (city, project, value))

        conditions = {
            "city": city,
            "project": project
        }
        config.update_datas(id, name, conditions, value)

        common.print_info("get id:%s, name:%s from cookies" % (id, name))
        # return render_template('user.html', id=id, name=name, form=form_update_data)

    if request.method == 'POST':
        file = request.files['file']
        filename = file.filename
        common.print_info("上传文件: %s" % filename)
        try:
            # file.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(filename)))
            excel = os.path.join(app.config['UPLOAD_FOLDER'], "%s_%s_%s_%s" % (common.current_time(fmt='%Y%m%d-%H%M%S-%f'), id, name, filename))
            file.save(excel)

            # 检查
            ret, info = excel_check(excel, titles_std=titles_std)
            if ret:
                project_name, date_power = info
                flash("%s 上传成功，项目名称：%s，时间力度：%s" % (filename, project_name, date_power))

                # 重命名文件
                filename_new = "%s_%s_%s_%s" % (date_power, project_name, id, name)
                excel_new = file_utils.replace_filename(excel, filename_new)
                file_utils.copy_file(excel, excel_new)

                # 源文件备份
                excel_backup = os.path.join("backups", os.path.basename(excel))
                file_utils.move_file(excel, excel_backup)
            else:
                flash(info)
        except Exception as e:
            flash("ERROR! %s" % e)


    # return render_template('user.html', form=form_update_data)
    return render_template('user.html', id=id, name=name, form=form_update_data)


if __name__ == '__main__':
    app.run(debug=True)

