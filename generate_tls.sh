#!/usr/bin/bash

echo "Generating TLS Certificate..."

sudo snap install --classic certbot
sudo ln -s /snap/bin/certbot /usr/bin/certbot
sudo certbot --nginx --non-interactive --agree-tos --email your-email@example.com --domain blog.vizallati.guru

echo "TLS Certificate Successfully Generated!"