# coding=utf-8

from Service import BaseService


class MyService(BaseService):

    TIMEOUT = 100
    def __init__(self,  uri = "/app",
                        serviceName = "app",
                 ):
        BaseService.__init__(self, uri = uri,serviceName = serviceName)

    def process(self, dictReq):
        name = dictReq.get("name")
        # ret = "hello!", self.serviceCall("http://127.0.0.1:5001/test",dictReq) # call other microservice
        ret = {"ret": "hello! %s" % name }
        return ret

if __name__ == "__main__":

    ms = MyService()
    ms.start()
