# coding=utf-8

import json

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




j = json.load(open("config.json","r"))
print j