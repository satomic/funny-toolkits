# coding=utf-8
import time
import json
import requests
import urllib3
import datetime
urllib3.disable_warnings()


import os


headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
}



def current_time(fmt='%Y-%m-%d %H:%M'):
    return datetime.datetime.now().strftime(fmt)

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
    scale_time = env_dist.get('scale_time')
    scale_num = int(env_dist.get('scale_num'))

    while True:
        time.sleep(5)
        print(current_time())
        current_scale = get_scale(app_url=app_url, auth=auth)
        if current_scale == scale_num:
            continue
        else:
            if current_time() == scale_time:
                print("it's %s now, need to scale up to %s" % (scale_time, scale_num))
                put_scale(app_url=app_url, num=scale_num, auth=auth)



if __name__ == "__main__":
    # app_url = 'https://47.75.169.54/v3/project/c-xc62x:p-92gdf/workloads/deployment:default:tps'
    # auth = ('token-xfmq9', 'lql8dj4ssrjgwrlqn86c2l5tgc4gggpbpqbxfpjsd2k556blt8wvqf')
    # print(get_scale(app_url=app_url, auth=auth))
    app()
