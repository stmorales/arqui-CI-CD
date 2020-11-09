cd ..
ls
cd ..
ls
cd /home/ec2-user/iic2173-proyecto-semestral-grupo-14
docker-compose -f production.yml down
docker stop $(docker ps -a -q)
