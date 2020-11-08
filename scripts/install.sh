docker container stop $(docker container ls -aq)
docker login -u AWS -p $pwd https://176269071650.dkr.ecr.us-east-1.amazonaws.com/backend-arqui
docker pull 176269071650.dkr.ecr.us-east-1.amazonaws.com/backend-arqui