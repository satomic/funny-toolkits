# coding=utf-8

import json
from databases.sqlite3_data import DataSqlite

class Config():

    # todo: 包装成抽象类，然后由不同的技术实现

    type_sqlite = "sqlite"
    type_json = "json"

    def __init__(self, config_file, db_file):
        self.db = DataSqlite(db_file)
        self.init()
        self.type = self.type_sqlite # sqlite/json

    def init(self):
        self.db.create_table()
        if not self.db.has_admin_id("satomic"):
            self.db.update_user(id="satomic",
                                name="satomic",
                                key="satomic",
                                table="admins")

    # 通用用户信息获取
    def __get_users_ids(self, user_type="users"):
        """
        :return: 返回所有普通用户的id列表  
        """
        return self.db.get_user_ids()

    def is_user(self, id):
        return self.db.has_user_id(id)

    def get_user_name_by_id(self, id, user_type="users"):
        return self.db.get_user_name_by_id(id)

    # 管理员信息获取
    def __get_admins_ids(self):
        return self.__get_users_ids(user_type="admins")

    def is_admin(self, id):
        return self.db.has_admin_id(id)

    def get_admin_name_by_id(self, id):
        return self.db.get_admin_name_by_id(id)

    def get_admin_key_by_id(self, id):
        return self.db.get_admin_key_by_id(id)

    def get_1st_admin_name(self):
        resp = self.db.get_admin_names()
        if resp:
            return resp[0]

    def update_user(self, id, name, key):
        self.db.update_user(id, name, key)


if __name__ == "__main__":
    config = Config("configs/config.json")
    # print(config.__get_users_ids())
    print(config.get_user_name("b"))
    # print(config.__get_admins_ids())
    print(config.get_admin_name("satomic"))
    print(config.is_admin("satomic"))
    print(config.is_user("satomic", user_type="admins"))
    print(config.is_user("a"))
    print(config.is_user("b"))
    print(config.is_user("c"))
    print(config.get_1st_admin_name())

    # print('satomic' in config.__get_admins_ids())