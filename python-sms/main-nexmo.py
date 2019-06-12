# coding=utf-8

import nexmo
# from nexmo import Client


client = nexmo.Client(key='356e202b', secret='MZNVCm1mttq5m3zx')

client.send_message({
    'from': 'Nexmo',
    'to': '8615026630181',
    'text': u'姚慧我爱你',
})