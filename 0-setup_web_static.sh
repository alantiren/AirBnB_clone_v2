#!/usr/bin/env bash
# Script to prepare web servers for web_static deployment

# Install Nginx if it's not already installed
apt-get update
apt-get install -y nginx

# Create necessary directories if they don't exist
mkdir -p /data/web_static/releases/test/
mkdir -p /data/web_static/shared/

# Create a fake HTML file for testing
echo "Holberton School" > /data/web_static/releases/test/index.html

# Create or recreate a symbolic link
ln -sf /data/web_static/releases/test/ /data/web_static/current

# Give ownership to the ubuntu user and group recursively
chown -R ubuntu /data/
chgrp -R ubuntu /data/

# Update Nginx configuration
printf %s "server {
    listen 80 default_server;
    listen [::]:80 default_server;
    add_header X-Served-By $HOSTNAME;
    root   /var/www/html;
    index  index.html index.htm;

    location /hbnb_static {
        alias /data/web_static/current;
        index index.html index.htm;
    }

    location /redirect_me {
        return 301 http://cuberule.com/;
    }

    error_page 404 /404.html;
    location /404 {
      root /var/www/html;
      internal;
    }
}" > /etc/nginx/sites-available/default

# Restart Nginx
service nginx restart
