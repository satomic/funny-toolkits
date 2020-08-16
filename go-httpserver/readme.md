# how to use
mount your local path into `/tmp` path in the container, then expose the port `8080`
```
docker run -p 8080:8080 -v /tmp/:/tmp/ satomic/httpserver-go
```


