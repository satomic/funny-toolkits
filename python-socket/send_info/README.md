you can access docker version here [python-socket](https://hub.docker.com/r/satomic/python-socket/)

---

# how to use
this image was build based on `python:2.7-alpine`, the key change is add a `socket_cs.py` in root path `/`. your running commond show be. 
* expecially the `<SERVER_IP>` should be interpreted. if you are running the docker in a public cloud env, you shoud set the `<SERVER_IP>` with INTERNAL_IP, otherwise, a ERROR will pop out. 
* `<MODE>` support two types `server` and `client`<br/>
```docker run -it --net host satomic/python-socket:2.7-alpine python /socket_cs.py <MODE> --host <SERVER_IP> --port <INTER_PORT>```

# demo 
trypically example is like below.
## server mode
```docker run -it --net host satomic/python-socket:2.7-alpine```
## client mode
```docker run -it satomic/python-socket:2.7-alpine python /socket_cs.py client --host 118.190.156.75```

# run with rancher
this can be deployed in k8s or rancher easily.<br/>
* for `server`, you just need to use the `hostNetwork: true`, and run with the default `CMD`.<br/>
* for `client`, you need to set `command` like `python /socket_cs.py client --host 172.31.164.130`, the IP is you can see in `server` log, if it is run in a pulibc cloud, the IP maybe the internal IP of the pod's host node, you can still change the IP to public IP of the host node.
