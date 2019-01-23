import logging
import requests
import json
from requests.exceptions import Timeout
# from py_zipkin.zipkin import create_http_headers_for_new_span

def serviceCall(serviceUri, dictRequest, timeout=600):

    logging.info("serviceCall start")
    headers = {"Content-type": "application/json"}

    proxies = {
        "http": None
    }

    try:
        # headers = create_http_headers_for_new_span()
        # headers.update({"Content-type": "application/json"})
        r = requests.post(url=serviceUri, data=json.dumps(dictRequest), timeout=timeout, headers=headers, proxies=proxies)
        rtCode = r.status_code
        try:
            rtText = json.loads(r.text)
        except:
            rtText = {"error": r.text}
    except Timeout:
        rtCode = 400
        rtText = {"error": "timeout={}".format(timeout)}
    except Exception as e:
        rtCode = 520
        rtText = {"error": str(e)}
    return rtText
    logging.info("serviceCall end: %s" % rtCode)

if __name__=="__main__":
    uri = "http://xx.xx.xx.xx/hello"
    dictRequest = {
        "fuck": "you"
    }
    ret = serviceCall(uri, dictRequest, timeout=5)
    print("ret: %s" % ret)