you can access docker version here [python-webhook-k8s](https://hub.docker.com/r/satomic/python-webhook-k8s/)

---

## this a webhook service for you to contrl your k8s cluster by POST json content.

- what you need to config is the `/usr/src/kubeconfig/kubeconfig.yaml` file, you need to mount it with a `configmap`
- and the default listening port is `8080`

### POST JSON format
```
 {
    "type": "apply",
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
