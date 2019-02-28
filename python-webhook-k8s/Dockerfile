FROM satomic/python:flask
WORKDIR /usr/src
RUN wget https://www.cnrancher.com/download/kubectl/kubectl_amd64-linux
RUN chmod +x kubectl_amd64-linux
COPY MicroService ./MicroService
COPY ServiceWebhook.py ./ServiceWebhook.py
CMD ["python","ServiceWebhook.py"]
