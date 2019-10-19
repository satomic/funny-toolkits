# coding=utf-8
import time
import json
import requests
import urllib3
urllib3.disable_warnings()


import os


headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
}


def put_scale(app_url, num, auth):
    data = {"scale": num}
    data = str(data).replace("'",'"')
    response = requests.put(app_url, headers=headers, data=data, verify=False, auth=auth)
    time.sleep(30)
    if response.reason == "OK":
        return True
    return False

def get_scale(app_url, auth):
    response = requests.get(app_url, headers=headers, verify=False, auth=auth)
    # print(response.reason)
    if response.reason == "OK":
        return json.loads(response.text).get("scale")
    return None


def app():
    app_url = 'https://47.75.169.54/v3/project/c-xc62x:p-92gdf/workloads/deployment:default:tps'
    auth=('token-xfmq9', 'lql8dj4ssrjgwrlqn86c2l5tgc4gggpbpqbxfpjsd2k556blt8wvqf')

    url = "http://47.244.191.68:30080/metric"
    # thred = 8

    env_dist = os.environ
    thred = int(env_dist.get('thred'))
    step1 = int(env_dist.get('step1'))
    step2 = int(env_dist.get('step2'))
    step3 = int(env_dist.get('step3'))

    while True:
        time.sleep(2)
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            request_tps = eval(response.text.split(" ")[-1])
            current_scale = get_scale(app_url=app_url, auth=auth)
            if request_tps >= thred:
                if current_scale == step1:
                    next_scale = step2
                    print("need to scale up to %s" % next_scale)
                    put_scale(app_url=app_url, num=next_scale, auth=auth)
                elif current_scale == step2:
                    next_scale = step3
                    print("need to scale up to %s" % next_scale)
                    put_scale(app_url=app_url, num=next_scale, auth=auth)
                else:
                    print("max scale")
            else:
                if current_scale == step3:
                    next_scale = step2
                    print("need to scale down to %s" % next_scale)
                    put_scale(app_url=app_url, num=next_scale, auth=auth)
                elif current_scale == step2:
                    next_scale = step1
                    print("need to scale down to %s" % next_scale)
                    put_scale(app_url=app_url, num=next_scale, auth=auth)
                else:
                    print("min scale")
            continue
        print("error!")

if __name__ == "__main__":
    # app_url = 'https://47.75.169.54/v3/project/c-xc62x:p-92gdf/workloads/deployment:default:tps'
    # auth = ('token-xfmq9', 'lql8dj4ssrjgwrlqn86c2l5tgc4gggpbpqbxfpjsd2k556blt8wvqf')
    # print(get_scale(app_url=app_url, auth=auth))
    app()
