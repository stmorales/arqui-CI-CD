# sudo curl -L https://github.com/docker/compose/releases/download/1.21.0/docker-compose-`uname -s`-`uname -m` | sudo tee /usr/local/bin/docker-compose > /dev/null
# sudo chmod +x /opt/bin/docker-compose
ls
cd home/ec2-user/
docker-compose -f iic2173-proyecto-semestral-grupo-14/production.yml up -d