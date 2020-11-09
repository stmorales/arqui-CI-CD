# sudo curl -L https://github.com/docker/compose/releases/download/1.21.0/docker-compose-`uname -s`-`uname -m` | sudo tee /usr/local/bin/docker-compose > /dev/null
# sudo chmod +x /opt/bin/docker-compose

cd ..
cd ..
cd /home/ec2-user/iic2173-proyecto-semestral-grupo-14
docker-compose -f production.yml up -d
docker-compose -f production.yml up -d