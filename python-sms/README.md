you can access docker version here [python-kafka](https://hub.docker.com/r/satomic/python-httpserver/)

---

default port is `8080`, you can specify another port with `CMD` of the run command:
```
docker run -it -p <HOST_PORT>:<HTTP_PORT> satomic/python-httpserver <HTTP_PORT>
```
