you can access docker version here [python-kafka](https://hub.docker.com/r/satomic/python-kafka/)

---

# how to use
this image was build based on `python:2.7-alpine`, the key change is add a `kafka-client.py` in root path `/`.
## key paras explanation
```
BROKERS = args.brokers.split(",")
ROLE = args.role
TOPIC = args.topic
GROUP = args.group
MSG = args.msg
TEST = args.test
```
* `brokers` kafka broker list, if you have more than one broker, it looks like `broker1,broker2,...,brokerN`
* `role` `p` or `c` is supported for producer and consumer
* `--topic`
* `--group`
* `--msg`
* `--test` default value is `false`, if `true` is setted, kafka msg will be produced every per second.

## for details you can use `-h` command
```
# docker run -it satomic/python-kafka:0.1 python /kafka-client.py -h
usage: kafka-client.py [-h] [--topic TOPIC] [--group GROUP] [--msg MSG]
                       [--test TEST]
                       brokers role

p/c

positional arguments:
  brokers        broker list with ',' splited
  role           only 'p' and 'c' are supported

optional arguments:
  -h, --help     show this help message and exit
  --topic TOPIC  kafka topic
  --group GROUP  kafka group
  --msg MSG      kafka topic
  --test TEST    if --test if true, producer with produce msg every per second

```

# demo 
trypically example is like below.
## consumer mode
```docker run -it satomic/python-kafka:0.1 python /kafka-client.py 47.105.135.136:32772 c```
## producer mode
```docker run -it satomic/python-kafka:0.1 python /kafka-client.py 47.105.135.136:32772 p --msg yaohui```

