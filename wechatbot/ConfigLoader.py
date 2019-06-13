# coding=utf-8

import json
import os


class Config(object):

    def __init__(self, config_file):
        with open(config_file, "r", encoding="utf-8") as f:
            self.json_obj = json.load(f)

        self.host_name = self.json_obj.get("host_name", None)
        self.groups = self.json_obj.get("groups", None)
        self.master_id = self.json_obj.get("master_id", None)
        self.add_request = self.json_obj.get("add_request", None)
        self.reply = self.json_obj.get("reply", None)
        self.weather = self.json_obj.get("weather", None)
        self.auto_reply = self.json_obj.get("auto_reply", None)







if __name__ == "__main__":
    c = Config(r"config.json")
    print(c.host_name)
    print(c.reply.keys())
    print(type("你好"))
    print("你好" in c.reply.keys())
    print(os.path.exists("C:/Users/yxfde/Desktop/我要是有钱该多好.png"))