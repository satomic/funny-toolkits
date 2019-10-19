# import urllib.parse
# import http.client
# import json
#
#
# test_data ={"scale": 1}
# test_data_url_encode = urllib.parse.urlencode(test_data)
# request_url = "https://47.75.169.54/v3/project/c-xc62x:p-92gdf/workloads/deployment:default:tps"
# conn = http.client.HTTPConnection('47.75.169.54')
# header = {
#     "Content-type": "application/x-www-form-urlencoded",
#     "Accept": "text/plain",
#     "token-xfmq9": "lql8dj4ssrjgwrlqn86c2l5tgc4gggpbpqbxfpjsd2k556blt8wvqf"
# }
# conn.request(method="POST", url=request_url, headers=header, body=test_data_url_encode)
# response = conn.getresponse()
# #print(response.status)
# #print(response.reason)
# res = response.read()
# print(res)
# resp = json.loads(res)
# print(resp)

import json
import requests
import urllib3
urllib3.disable_warnings()

headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
}

data = {"scale": 3}
data = str(data).replace("'",'"')
response = requests.put('https://47.75.169.54/v3/project/c-xc62x:p-92gdf/workloads/deployment:default:tps', headers=headers, data=data, verify=False, auth=('token-xfmq9', 'lql8dj4ssrjgwrlqn86c2l5tgc4gggpbpqbxfpjsd2k556blt8wvqf'))
# print(response.status)
print(response.reason)
# res = response.read()
# print(res)
# resp = json.loads(res)
# print(resp)
