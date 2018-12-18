# clear old version
docker kill python-httpserver
docker rm python-httpserver

# build new one
docker build -t python-httpserver .

# push
# docker push python-httpserver

# run 
docker run -it -p 8080:8080 --name python-httpserver python-httpserver
