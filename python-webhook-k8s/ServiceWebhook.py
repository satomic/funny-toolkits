# coding=utf-8

from MicroService.Service import BaseService
import os
import datetime
from ShellCaller import ShellCaller

class ServiceFace(BaseService):

    TIMEOUT = 100

    def __init__(self, uri="/webhook", service_name="webhook"):
        BaseService.__init__(self, uri=uri, service_name=service_name, ver = "v0.0.1", port = 8080)
        self.sc = ShellCaller()

    def process(self, dictReq):
        # ret = "hello!", self.serviceCall("http://127.0.0.1:5001/test",dictReq) # call other microservice
        # dictReq = {
        #  "type": "create",
        #  "json": "<DETAILS>"
        # }
        nowtime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        log = "%s %s" % (nowtime, dictReq)
        print(log.replace("'",'"').replace('u"','"'))

        # a = {}


        if not (dictReq.has_key("type") and dictReq.has_key("json")):
            return "paras illegal"
        if dictReq.get("type") not in self.sc.TYPE_LIST:
            return "type illegal"
        return {"result": `self.sc.run_kubectl_json(dictReq.get("type"), dictReq.get("json"))`}

        return {nowtime: "success"}

if __name__ == "__main__":
    print("webhook service started, please post info to http://<SERVER_IP>/webhook")
    ms = ServiceFace()
    ms.start()
