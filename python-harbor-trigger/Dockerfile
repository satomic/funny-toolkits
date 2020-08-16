FROM satomic/python:flask
WORKDIR /usr/src
RUN wget https://docs.rancher.cn/download/kubernetes/linux-amd64-v1.17.6-kubectl
RUN chmod +x linux-amd64-v1.17.6-kubectl
RUN mv linux-amd64-v1.17.6-kubectl kubectl
RUN mkdir kubeconfig
# COPY kubeconfig/kubeconfig.yaml .kubeconfig/kubeconfig.yaml
COPY MicroService ./MicroService
COPY ShellCaller.py ./ShellCaller.py
COPY ServiceWebhook.py ./ServiceWebhook.py
# COPY config.json ./config.json
CMD ["python","ServiceWebhook.py"]


FROM satomic/python:flask
WORKDIR /usr/src
RUN wget https://docs.rancher.cn/download/kubernetes/linux-amd64-v1.17.6-kubectl
RUN chmod +x linux-amd64-v1.17.6-kubectl
RUN mv linux-amd64-v1.17.6-kubectl kubectl
RUN mkdir kubeconfig
# COPY kubeconfig/kubeconfig.yaml .kubeconfig/kubeconfig.yaml
COPY MicroService ./MicroService
COPY ShellCaller.py ./ShellCaller.py
COPY ServiceWebhook.py ./ServiceWebhook.py
# COPY config.json ./config.json
CMD ["python","ServiceWebhook.py"]