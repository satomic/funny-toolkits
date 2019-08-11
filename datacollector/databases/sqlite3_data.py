#coding=utf-8

from databases.sqlite3_utils import EasySqlite
import common.common as common
import common.hash_utils as hash_utils

class DataSqlite(EasySqlite):

    table_history = "history"
    table_datas = "datas"
    table_users = "users"
    table_admins = "admins"

    def create_table(self):
        structure_data = "( id TEXT, \
                        uuid TEXT, \
                        name TEXT, \
                        city TEXT, \
                        project TEXT, \
                        value TEXT, \
                        time_value TEXT, \
                        condition_extension TEXT, \
                        value_extension TEXT, \
                        timestamp TEXT)"
        structure_user = "( id TEXT, \
                        name TEXT, \
                        key TEXT, \
                        timestamp TEXT)"
        table_define = {
            self.table_history: structure_data,
            self.table_datas: structure_data,
            self.table_users: structure_user,
            self.table_admins: structure_user
        }
        try:
            table_names = self.get_all_table_names()
            for table_name, structure in table_define.items():
                if not table_name in table_names:
                    self.execute("CREATE TABLE %s %s" % (table_name, structure))
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
        values["timestamp"] = current_time
        values["value"] = value
        if value_extension:
            values["value_extension"] = common.gen_json_str(value_extension)

        self.update(table=self.table_datas, values=values, conditions=conditions)
        values.update(conditions)
        self.insert(table=self.table_history, values=values)

    def update_user(self, id, name, key, table="users"):
        conditions = {"id": id}
        user = {"name": name}
        current_time = common.current_time()
        user["timestamp"] = current_time
        user["key"] = key
        self.update(table=table, values=user, conditions=conditions)

    def get_users(self, table="users"):
        return self.query(table=table)

    def get_user_ids(self, table="users"):
        resp = self.get_users(table=table)
        return self.get_column_list_from_resp_dict_list(resp, "id")

    def get_user_names(self, table="users"):
        resp = self.get_users(table=table)
        return self.get_column_list_from_resp_dict_list(resp, "name")

    def has_user_id(self, id, table="users"):
        return id in self.get_user_ids(table=table)

    def has_user_name(self, name, table="users"):
        return name in self.get_user_names(table=table)

    def get_user_name_by_id(self, id, table="users"):
        if not self.has_user_id(id, table=table):
            return None
        resp = self.query(table=table, columns="name", conditions={"id": id})
        return resp[0].get("name")

    def get_user_key_by_id(self, id, table="users"):
        if not self.has_user_id(id, table=table):
            return None
        resp = self.query(table=table, columns="key", conditions={"id": id})
        return resp[0].get("key")

    def get_admins(self, table="admins"):
        return self.get_users(table=table)

    def get_admin_ids(self, table="admins"):
        return self.get_user_ids(table=table)

    def get_admin_names(self, table="admins"):
        return self.get_user_names(table=table)

    def has_admin_id(self, id, table="admins"):
        return self.has_user_id(id, table=table)

    def has_admin_name(self, name, table="admins"):
        return self.has_user_name(name, table=table)

    def get_admin_name_by_id(self, id, table="admins"):
        return self.get_user_name_by_id(id, table=table)

    def get_admin_key_by_id(self, id, table="admins"):
        return self.get_user_key_by_id(id, table=table)

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

    print(db.get_all_table_names())
    db.update_user("satomic", "姚慧", "123321")
    print(db.get_users())
    print(db.get_user_ids())
    print(db.get_user_names())
    print(db.get_name_by_id("satomic"))