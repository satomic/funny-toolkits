FROM satomic/python:flask
WORKDIR /usr/src
RUN wget https://www.cnrancher.com/download/kubectl/kubectl_amd64-linux
RUN chmod +x kubectl_amd64-linux
RUN mv kubectl_amd64-linux kubectl
RUN mkdir kubeconfig
COPY kubeconfig/kubeconfig.yaml .kubeconfig/kubeconfig.yaml
COPY MicroService ./MicroService
COPY ShellCaller.py ./ShellCaller.py
COPY ServiceWebhook.py ./ServiceWebhook.py
CMD ["python","ServiceWebhook.py"]
