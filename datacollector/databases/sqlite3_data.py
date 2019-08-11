#coding=utf-8

from databases.sqlite3_utils import EasySqlite
import common.common as common

class DataSqlite(EasySqlite):


    def create_table(self):
        table_define = "( id TEXT, \
                        name TEXT, \
                        city TEXT, \
                        project TEXT, \
                        value TEXT, \
                        time_value TEXT, \
                        time_update TEXT)"
        try:
            self.execute("CREATE TABLE datas %s" % table_define)
            self.execute("CREATE TABLE history %s" % table_define)
        except Exception as e:
            common.print_warn(e)

    def update_datas(self, id, name, values):
        values["time_update"] = common.current_time()
        conditions = {"id": id, "name": name}
        self.update(table="datas", values=values, conditions=conditions)
        values.update(conditions)
        self.insert(table="history", values=values)




if __name__ == '__main__':

    db = DataSqlite('database.db3')
    db.create_table()

    values = {
        "city": "上海",
        "project": "项目",
        "value": "789",
        "time_value":"20190810"
    }

    db.update_datas(id="satomic", name="satomic", values=values)
    history = db.query(table="history", columns=["value"])
    if history:
        for i in history:
            print(i)