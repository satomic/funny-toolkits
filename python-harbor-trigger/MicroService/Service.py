# coding=utf-8

import flask
import logging
import time
import os
import requests
import traceback
from serviceRequest import serviceCall
from deco import timeout


class  BaseService(object):
    '''
    the base class of micro service
    two for extension
        1) uri: the entrance of the service, like '/hello'
        2) process: what to do in the service
    '''

    TIMEOUT = 100
    def __init__(self,
                        uri,
                        service_name = None,
                        ver = "1.0.0",
                        host = "0.0.0.0",
                        port = 5000,
                        threaded = False,
                 ):
        self.traceID = None
        self.host = host
        self.port = port
        self.uri = uri
        self.serviceVer = ver
        self.threaded = threaded
        if service_name:
            self.serviceName = service_name
        else:
            self.serviceName = os.path.basename(os.path.normcase(uri)).lower()

        self.app = flask.Flask(self.serviceName)
        self.errorTags = []

    def default_exception_handler(self, ex):
        logging.error(traceback.format_exc())

    def start(self):
        if self.uri is None:
            logging.warning("uri empty, please set uri like '/hello'")
            return
        self.app.add_url_rule(self.uri, self.serviceName, self.processWrap, methods=["POST"])
        # 这个是为特定的service所保留的一个测试入口，验证是否可用
        self.app.add_url_rule(self.uri+"/hello", "TestHello", self.testHello, methods=["GET"])
        logging.info("service starting with uri %s" % self.uri)
        self.app.run(host=self.host, port=self.port, threaded=self.threaded, debug=False)

    def testHello(self):
        return "hello via %s.\n(if you see this, means your service is avaiable)\n" % self.uri

    def processWrap(self):
        logging.info("service start <%s>" % self.serviceName)
        dictReq = flask.request.get_json()

        # 1.0 check input
        if not isinstance(dictReq, dict):
            dictRet = {"error": "request msg is not a dict"}
            # self.zipkin.update_tags(retCode=400)
            # self.zipkin.update_tags(error=dictRet["error"])
            return flask.jsonify(**dictRet)

        # 2.0 service process
        try:
            dictRet = self.process(dictReq)
        except:
            dictRet = {
                "error": "error in process",
                "trace": "%s" % traceback.format_exc()
            }
            logging.error("error trace: %s" % dictRet["trace"])
            return flask.jsonify(**dictRet)

        # 3.0 output check
        if not isinstance(dictRet, dict):
            dictRet = {
                "error": "error in output",
                "ret": str(dictRet)
            }

        dictRet.update({"ver": self.serviceVer})
        return flask.jsonify(**dictRet)

    @timeout(TIMEOUT)
    def process(self, dictReq):
        pass

    def tagError(self, strError):
        self.errorTags.append(strError)

    def serviceCall(self, serviceUri, dictRequest, timeout=600):
        # 0 input check
        if not isinstance(dictRequest, dict):
            return (500, {"error": "error in client input"})
        # 1 service call
        serviceName = os.path.basename(os.path.normcase(serviceUri)).lower()
        ret = serviceCall(serviceUri, dictRequest, timeout)
        return ret

if __name__ == "__main__":

    pass