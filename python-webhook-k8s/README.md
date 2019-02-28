you can access docker version here [python-webhook-k8s](https://hub.docker.com/r/satomic/python-webhook-k8s/)

已经构建好的镜像版本参考[python-webhook-k8s](https://hub.docker.com/r/satomic/python-webhook-k8s/)，自带dockerfile，你可以自己构建一个镜像直接就可以使用

---

## this a webhook service for you to contrl your k8s cluster by POST json content. 
- what you need to config is the `/usr/src/kubeconfig/kubeconfig.yaml` file, you need to mount it with a `configmap`
- and the default listening port is `8080`

## 这是一个微服务应用容器，可以docker run，也可以部署在k8s中，向这个微服务POST json消息，就可以控制集群，返回值就是集群的响应值
- 通过给它配置`/usr/src/kubeconfig/kubeconfig.yaml`文件，就可以连接你需要控制的集群
- 默认监听端口为`8080`


### POST JSON format POST消息体格式
<OPERATE TYPE> list, 可选的操作类型如下
```["version", "create", "delete", "apply"]```
```
 {
    "type": "<OPERATE TYPE>",
    "json": {
        <KUBECTL JSON CONTENT>
        # you can get content by
        # kubectl get deploy xxx -o json
    }
}
```


### demo JSON
after that, you can POST a JSON like
```
{
    "type": "apply",
    "json": {
        "apiVersion": "extensions/v1beta1",
        "kind": "Deployment",
        "metadata": {
            "name": "nginx",
            "namespace": "default"
        },
        "spec": {
            "replicas": 1,
            "template": {
            "metadata": {
                "labels": {
                    "workload.user.cattle.io/workloadselector": "deployment-default-nginx"
                }
            },
                "spec": {
                    "containers": [
                        {
                            "image": "nginx",
                            "imagePullPolicy": "Always",
                            "name": "nginx"
                        }
                    ]
                }
            }
        }
    }
}
```
