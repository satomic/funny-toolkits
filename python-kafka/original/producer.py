# coding=utf-8
from kafka import KafkaProducer
from kafka.errors import KafkaError

producer = KafkaProducer(bootstrap_servers=['47.105.135.136:32772'])
# producer.send('project', 'this is just a test')
future = producer.send('k8saudit', 'this is just a test')
try:
    record_metadata = future.get(timeout=10)
    print (record_metadata.topic)
    print (record_metadata.partition)
    print (record_metadata.offset)
except KafkaError:
    # log.exception()
    pass
