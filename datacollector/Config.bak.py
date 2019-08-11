# coding=utf-8

import json
from databases.sqlite3_data import DataSqlite

class Config():

    # todo: 包装成抽象类，然后由不同的技术实现

    type_sqlite = "sqlite"
    type_json = "json"

    def __init__(self, config_file, db_file):
        self.config = json.load(open(config_file,"r"))
        self.db = DataSqlite(db_file)
        self.db.create_table()
        self.type = self.type_sqlite # sqlite/json

    def get_config(self):
        return self.config

    # 通用用户信息获取
    def __get_users_ids(self, user_type="users"):
        """
        :return: 返回所有普通用户的id列表  
        """
        return self.config.get(user_type).keys()


    def is_user(self, id, user_type="users"):
        if id in self.__get_users_ids(user_type=user_type):
            return True
        return False

    def get_user_info(self, id, user_type="users"):
        if self.is_user(id, user_type=user_type):
            return self.config.get(user_type).get(id)
        return None

    def get_user_name(self, id, user_type="users"):
        info = self.get_user_info(id, user_type=user_type)
        if info:
            return info.get("name")
        return None

    def get_user_key(self, id, user_type="users"):
        info = self.get_user_info(id, user_type=user_type)
        if info:
            # print(info)
            return info.get("key")
        return None


    # 管理员信息获取
    def __get_admins_ids(self):
        return self.__get_users_ids(user_type="admins")

    def is_admin(self, id):
        return self.is_user(id, user_type="admins")

    def get_admin_name(self, id):
        return self.get_user_name(id, user_type="admins")

    def get_admin_key(self, id):
        return self.get_user_key(id, user_type="admins")

    def get_1st_admin_name(self):
        return self.get_user_name(list(self.__get_admins_ids())[0], user_type="admins")

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