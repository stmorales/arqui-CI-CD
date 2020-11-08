docker container stop $(docker container ls -aq)
aws ecr get-login-password --region us-east-1 | docker login -u AWS --password-stdin https://176269071650.dkr.ecr.us-east-1.amazonaws.com/backend-arqui
docker pull 176269071650.dkr.ecr.us-east-1.amazonaws.com/backend-arqui