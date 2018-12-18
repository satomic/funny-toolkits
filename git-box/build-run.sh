# clear old version
docker kill git-box
docker rm git-box

# build new one
docker build -t satomic/git-box .

# push
docker push satomic/git-box

# run 
docker run -it --name git-box satomic/git-box
