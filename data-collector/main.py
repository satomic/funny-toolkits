# coding=utf-8

from MicroService.Service import BaseService
import os
import datetime

class ServiceFace(BaseService):

    TIMEOUT = 100

    def __init__(self, uri="/webhook", service_name="webhook"):
        BaseService.__init__(self, uri=uri, service_name=service_name, ver = "v0.0.1", port = 80)

    def process(self, dictReq):
        # ret = "hello!", self.serviceCall("http://127.0.0.1:5001/test",dictReq) # call other microservice
        # dictReq = {
        #  "type": "local/url",
        #  "path": "path"
        # }
        nowtime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        log = "%s %s" % (nowtime, dictReq)
        print(log.replace("'",'"').replace('u"','"'))
        return {nowtime: "success"}

if __name__ == "__main__":
    print("webhook service started, please post info to http://<SERVER_IP>/webhook")
    ms = ServiceFace()
    ms.start()
