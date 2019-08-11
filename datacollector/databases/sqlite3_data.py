#coding=utf-8

from databases.sqlite3_utils import EasySqlite
import common.common as common
import common.hash_utils as hash_utils

class DataSqlite(EasySqlite):


    def create_table(self):
        table_define = "( id TEXT, \
                        uuid TEXT, \
                        name TEXT, \
                        city TEXT, \
                        project TEXT, \
                        value TEXT, \
                        time_value TEXT, \
                        condition_extension TEXT, \
                        value_extension TEXT, \
                        time_update TEXT)"
        try:
            self.execute("CREATE TABLE datas %s" % table_define)
            self.execute("CREATE TABLE history %s" % table_define)
        except Exception as e:
            common.print_warn(e)

    def update_datas(self, id, name, conditions, value, condition_extension={}, value_extension={}):
        # 出去变化值之外的所有条件值
        conditions.update({"id": id, "name": name})
        if condition_extension:
            conditions["condition_extension"] = common.gen_json_str(condition_extension)

        # 变化值
        current_time = common.current_time()
        uuid = "%s-%s" % (hash_utils.hash(conditions, length=8), hash_utils.hash(current_time, length=8))
        values = { "uuid": uuid }
        values["time_update"] = current_time
        values["value"] = value
        if value_extension:
            values["value_extension"] = common.gen_json_str(value_extension)

        self.update(table="datas", values=values, conditions=conditions)
        values.update(conditions)
        self.insert(table="history", values=values)




if __name__ == '__main__':

    db = DataSqlite('database.db3')
    db.create_table()

    conditions = {
        "city": "上海",
        "project": "项目",
        "time_value":"20190810"
    }
    condition_extension = {"age": 17}
    value_extension = {"height": 164, "weight": 60}

    db.update_datas(id="yaohui", name="姚慧", conditions=conditions, value=1231214124, \
                    condition_extension=condition_extension, \
                    value_extension=value_extension)
    history = db.query(table="history", columns=["name", "value"])
    if history:
        for i in history:
            print(i)