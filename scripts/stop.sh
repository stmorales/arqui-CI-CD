docker-compose -f home/ec2-user/production.yml down
docker stop $(docker ps -a -q)
