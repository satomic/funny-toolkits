# coding=utf-8

from MicroService.Service import BaseService
import os
import datetime
import json
from ShellCaller import ShellCaller

class ServiceFace(BaseService):

    TIMEOUT = 100

    def __init__(self, uri="/webhook", service_name="webhook"):
        BaseService.__init__(self, uri=uri, service_name=service_name, ver = "v0.0.1", port = 8080)
        self.deploy_config = json.load(open("config.json","r"))
        self.sc = ShellCaller()

    def process(self, dictReq):
        # ret = "hello!", self.serviceCall("http://127.0.0.1:5001/test",dictReq) # call other microservice
        # dictReq = {
        #  "type": "local/url",
        #  "path": "path"
        # }
        nowtime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        log = "%s %s" % (nowtime, dictReq)
        print(log.replace("'", '"').replace('u"', '"'))

        # json sample
        json_from_harbor = {
            "occur_at": 1592201805,
            "operator": "admin",
            "type": "pushImage",
            "event_data": {
                "repository": {
                    "date_created": 1592201805,
                    "repo_type": "public",
                    "repo_full_name": "myapps/busybox",
                    "namespace": "myapps",
                    "name": "busybox"
                },
                "resources": [{
                    "resource_url": "106.14.99.36/myapps/busybox:latest",
                    "tag": "latest",
                    "digest": "sha256:fd4a8673d0344c3a7f427fe4440d4b8dfd4fa59cfabbd9098f9eb0cb4ba905d0"
                }]
            }
        }


        if dictReq.get("type") != "pushImage":
            return None
        else:
            if dictReq.get("event_data").get("repository").get("repo_full_name") != self.deploy_config.get("repo_full_name"):
                return None
            else:
                image_resource_url = dictReq.get("event_data").get("resources")[0].get("resource_url")
                print("new image pushed: %s" % image_resource_url)
                operation = self.deploy_config.get("operation")

                # update image
                operation["json"]["spec"]["template"]["spec"]["containers"][0]["image"] = image_resource_url
                print("operation: %s" % operation)

                return {"result": `self.sc.run_kubectl_json(operation.get("type"), operation.get("json"))`}



if __name__ == "__main__":
    print("webhook service started, please post info to http://<SERVER_IP>/webhook")
    ms = ServiceFace()
    ms.start()
