#!/usr/bin/bash

MAIN_SERVICE_PORT=5000
BACKUP_SERVICE_PORT=5001
MAIN_SERVICE_NAME=web_app
BACKUP_SERVICE_NAME=web_app_backup

stop_server() {
  server="$1"
  echo "Stopping server: $server"
  sudo docker-compose stop "$server"
  sudo docker-compose rm -f "$server"
  container_name=$(sudo docker images | grep "$server" | cut -d ' ' -f 1)
  sudo docker rmi -f "$container_name"
#  sudo docker builder prune -f
}

start_server() {
  echo "Starting server: $1 ..."
  sudo docker-compose up -d --no-deps --build "$1"
  sleep 10
}

switch_upstream_server() {
  echo "Switching from upstream server running on port: $1 to server running on port: $2"
  sudo sed -i "s/$1/$2/g /etc/nginx/sites-available/default"
  sudo nginx -s reload
}


start_server $BACKUP_SERVICE_NAME
switch_upstream_server $MAIN_SERVICE_PORT $BACKUP_SERVICE_PORT

echo "Getting statuses of running containers"
sudo docker ps

stop_server $MAIN_SERVICE_NAME
start_server $MAIN_SERVICE_NAME
switch_upstream_server $BACKUP_SERVICE_PORT $MAIN_SERVICE_PORT

stop_server $BACKUP_SERVICE_NAME


