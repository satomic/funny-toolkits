# coding=utf-8

import os
import traceback
import yaml
import json
import random
import string

class ShellCaller(object):

    TYPE_LIST = ["version", "create", "delete", "apply"]

    def __init__(self):
        self.run_shell("mkdir yamls")
        self.run_shell("touch history.log")

    def run_shell(self, shell_cmd):
        try:
            ret = os.system(shell_cmd)
        except Exception,e:
            return traceback.format_exc(e)
        return ret

    def run_kubectl(self, type, yaml_file):
        '''
        :param type: TYPE_LIST
        :param yaml_file: yaml file path
        :return: kubectl exec result
        '''
        if not ( os.path.exists(yaml_file) and os.path.isfile(yaml_file) ):
            return "%s does not exist or not a file" % yaml_file
        cmd = "./kubectl --kubeconfig=kubeconfig.yaml %s %s" % (type, yaml_file)
        print("cmd: %s" % cmd)
        return self.run_shell(cmd)

    def run_kubectl_json(self, type, json_content):
        # print type(json_content)
        if type not in self.TYPE_LIST:
            return "%s not in %s" % (type, self.TYPE_LIST)
        if not isinstance(json_content, dict):
            return "%s is not a json file" % json_content
        # 产生随机文件名
        ran_str = ''.join(random.sample(string.ascii_letters + string.digits, 8))
        json_file = "yamls/%s.json" % ran_str
        with open(json_file,"w") as  f:
            json.dump(json_content, f)
        return self.run_kubectl(type, json_file)

if __name__ == "__main__":
    sc = ShellCaller()
    print sc.run_shell("ls -l")
    # print sc.run_kubectl("create", "./Dockerfile")
    print sc.run_kubectl_json("create", {"haha":"xixi"})
