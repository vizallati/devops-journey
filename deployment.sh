#!/usr/bin/bash


echo "Starting backup server..."
sudo docker-compose up -d web_app_backup
# todo: add checks for status of container
echo "Switching to backup server"
sudo sed -i s/5000/5001/g /etc/nginx/sites-available/default
sudo nginx -s reload

echo "Stopping main server"
sudo docker-compose stop web_app
sudo docker-compose rm -f web_app

echo "Rebuilding main server"
sudo docker-compose up -d --no-deps --build web_app
sleep 10

echo "Switching to main server"
sudo sed -i s/5001/5000/g /etc/nginx/sites-available/default
sudo nginx -s reload


echo "Stopping backup server"
sudo docker-compose stop web_app_backup
sudo docker-compose rm -f web_app_backup


