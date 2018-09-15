#coding=utf-8
from kafka import KafkaConsumer
consumer = KafkaConsumer('k8saudit',
                         group_id='my-group',
                         bootstrap_servers=['47.105.135.136:32772']) # 这二个port为brokers的二个端口
# print message.value
for message in consumer:
    print ("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
                                          message.offset, message.key,
                                          message.value))

