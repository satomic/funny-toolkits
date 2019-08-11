#coding=utf-8

import sqlite3
import common.common as common

class EasySqlite:
    """
    sqlite数据库操作工具类
    database: 数据库文件地址，例如：db/mydb.db
    """
    _connection = None

    def __init__(self, database):
        # 连接数据库
        self._connection = sqlite3.connect(database)

    def _dict_factory(self, cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    def execute(self, sql, args=[], result_dict=True, commit=True) -> list:
        """
        执行数据库操作的通用方法
        Args:
        sql: sql语句
        args: sql参数
        result_dict: 操作结果是否用dict格式返回
        commit: 是否提交事务
        Returns:
        list 列表，例如：
        [{'id': 1, 'name': '张三'}, {'id': 2, 'name': '李四'}]
        """
        if result_dict:
            self._connection.row_factory = self._dict_factory
        else:
            self._connection.row_factory = None
        # 获取游标
        _cursor = self._connection.cursor()
        # 执行SQL获取结果
        _cursor.execute(sql, args)
        if commit:
            self._connection.commit()
        data = _cursor.fetchall()
        _cursor.close()
        return data

    def gen_column_segment(self, columns=["*"]):
        return ", ".join(columns)

    def gen_condition_segment(self, conditions={}):
        if conditions and isinstance(conditions, dict):
            condition = []
            for key,value in conditions.items():
                condition.append("%s='%s'" % (key, value))
            sql = " and ".join(condition)
            return "where %s" % sql
        return ""

    def gen_values_segment(self, values, type="insert"):
        if type == "insert":
            key_list = list(values.keys())
            value_list = []
            for key in key_list:
                value_list.append("'%s'" % values.get(key))
            sql_value = ", ".join(key_list)
            sql_key = ", ".join(value_list)
            return "( %s ) values ( %s )" % (sql_value, sql_key)
        elif type == "update":
            condition = []
            for key, value in values.items():
                condition.append("%s='%s'" % (key, value))
            return ", ".join(condition)
        else:
            return None

    def query(self, table, columns=["*"], conditions={}):
        column_segment = self.gen_column_segment(columns)
        condition_segment = self.gen_condition_segment(conditions)
        sql = "select %s from %s %s" % (column_segment, table, condition_segment)
        common.print_info(sql)
        return self.execute(sql)

    def insert(self, table, values={}):
        """
        :param datas: {city, project, value, time_value}
        :return: 
        """
        if values and isinstance(values, dict):
            values_segment = self.gen_values_segment(values)
            sql = "insert into %s %s" % (table, values_segment)
            common.print_info(sql)
            self.execute(sql)

    def update(self, table, values={}, conditions={}):
        # 先按照条件查询，看是否有数据
        if self.query(table, conditions=conditions):
            # 如果有数据，就更新
            value_segment = self.gen_values_segment(values, type="update")
            condition_segment = self.gen_condition_segment(conditions)
            sql = """update %s set %s %s""" % (table, value_segment, condition_segment)
            common.print_info(sql)
            self.execute(sql)
        else:
            # 否则就插入
            values.update(conditions)
            self.insert(table, values=values)



if __name__ == '__main__':
    db = EasySqlite('database.db3')
    # print(db.execute("select name from sqlite_master where type=?", ['table']))
    # print(db.execute("pragma table_info([user])"))
    # print(db.execute("insert into user(id, name, password) values (?, ?, ?)", [2, "李四", "123456"]))
    # print(db.execute("select id, name userName, password pwd from user"))
    # print(db.execute("select * from user", result_dict=False))
    # print(db.execute("select * from user"))
    # db.create_table()
    data = {
        "id": "satomic",
        "name": "satomic",
        "city": "上海",
        "project": "项目",
        "value": "123",
        "time_value":"20190810"
    }
    # db.insert_data(data)

    history = db.update("datas",values={"value":456},conditions={"id":"satomic"})
    if history:
        for i in history:
            print(i)