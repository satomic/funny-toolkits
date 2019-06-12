from python:3.5-alpine
run pip install -U wxpy -i "https://pypi.doubanio.com/simple/"
workdir /srv
copy wechatbot.py .
cmd ["python", "wechatbot.py"]
