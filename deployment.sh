#!/usr/bin/bash


echo "Starting backup server..."
sudo docker-compose up -p default -d web_app_backup
# todo: add checks for status of container
echo "Switching to backup server"
sudo sed -i s/5000/5001/g /etc/nginx/sites-available/default
sudo nginx -s reload

echo "Rebuilding main server"
sudo docker-compose up -p default -d --build --force-recreate web_app
sleep 10

echo "Switching to main server"
sudo sed -i s/5001/5000/g /etc/nginx/sites-available/default
sudo nginx -s reload


echo "Stopping backup server"
sudo docker-compose stop web_app_backup
sudo docker-compose rm web_app_backup


