# coding=utf-8

from datetime import datetime
from elasticsearch6 import Elasticsearch

# 客户端连接
es = Elasticsearch(["47.75.216.239"],port='9200')

# 数据
doc = {
    'author': 'kimchy',
    'text': 'Elasticsearch: cool. bonsai cool.',
    'timestamp': datetime.now(),
}

# 往es中的test-index更新doc数据
res = es.index(index="test-index", doc_type='tweet', id=1, body=doc)
print(res['result'])

# 查询test-index中的第1条内容（用户数据）
res = es.get(index="test-index", doc_type='tweet', id=1)
print(res['_source'])

es.indices.refresh(index="test-index")

# 通过query条件获取元数据
res = es.search(index="test-index", body={"query": {"match_all": {}}})
print("Got %d Hits:" % res['hits']['total'])

# 逐条打印数据
for hit in res['hits']['hits']:
    print("%(timestamp)s %(author)s: %(text)s" % hit["_source"])
