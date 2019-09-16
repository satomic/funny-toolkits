#coding=utf-8

from kafka import KafkaConsumer
from kafka import KafkaProducer
from kafka.errors import KafkaError

import argparse
import traceback
import time
import datetime

# parser.add_argument('host', type=str, help="socket server IP") must be set
# parser.add_argument('--host', type=str, help="socket server IP") can be free

parser = argparse.ArgumentParser(description='p/c')
parser.add_argument('brokers', type=str, help="broker list with ',' splited")
parser.add_argument('role', type=str, help="only 'p' and 'c' are supported")
parser.add_argument('--topic', type=str, default = "default_kafka_topic", help="kafka topic")
parser.add_argument('--group', type=str, default = "default_kafka_group", help="kafka group")
parser.add_argument('--msg', type=str, default = "default kafka msg", help="kafka msg")
parser.add_argument('--test', type=str, default = "false", help="if --test if true, producer with produce msg every per second")
args = parser.parse_args()

BROKERS = args.brokers.split(",")
ROLE = args.role
TOPIC = args.topic
GROUP = args.group
MSG = args.msg
TEST = args.test

if ROLE == "p":
    producer = KafkaProducer(bootstrap_servers=BROKERS)
    while True:
        future = producer.send(TOPIC, MSG if TEST == "false" else datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f ') + MSG)
        try:
            record_metadata = future.get(timeout=10)
            print("topic:%s, partition:%s, offset:%s, msg:%s" % (record_metadata.topic, record_metadata.partition, record_metadata.offset, MSG))
        # except KafkaError:
        except Exception:
            print(traceback.format_exc())
        
        if TEST == "false":
            break
        time.sleep(1)

if ROLE == "c":
    consumer = KafkaConsumer(TOPIC,
                             group_id=GROUP,
                             bootstrap_servers=BROKERS) 
    # print message.value
    for message in consumer:
        print ("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
                                              message.offset, message.key,
                                              message.value.decode('utf8')))
