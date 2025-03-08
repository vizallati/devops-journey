#!/usr/bin/bash


echo "Starting backup server..."
sudo docker-compose up -d --build web_app_backup
sleep 20
# todo: add checks for status of container
echo "Switching to backup server"
sudo sed -i s/5000/5001/g /etc/nginx/sites-available/default
sudo nginx -s reload

echo "Stopping main server"
sudo docker-compose stop web_app
sudo docker-compose rm -f web_app
container_name=$(sudo docker images | grep web_app | cut -d ' ' -f 1)
sudo docker rmi -f "$container_name"

echo "Rebuilding main server"
sudo docker-compose up -d --no-deps --build web_app
sleep 20

echo "Switching to main server"
sudo sed -i s/5001/5000/g /etc/nginx/sites-available/default
sudo nginx -s reload


echo "Stopping backup server"
sudo docker-compose stop web_app_backup
sudo docker-compose rm -f web_app_backup
container_name=$(sudo docker images | grep web_app_backup | cut -d ' ' -f 1)
sudo docker rmi -f "$container_name"


