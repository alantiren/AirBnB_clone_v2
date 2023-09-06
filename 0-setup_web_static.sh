#!/usr/bin/env bash
# Script to prepare web servers for web_static deployment

# Install Nginx if it's not already installed
if ! [ -x "$(command -v nginx)" ]; then
    apt-get update
    apt-get -y install nginx
fi

# Create necessary directories if they don't exist
mkdir -p /data/web_static/releases/test/
mkdir -p /data/web_static/shared/

# Create a fake HTML file for testing
echo -e "<html>\n  <head>\n  </head>\n  <body>\n    Holberton School\n  </body>\n</html>" > /data/web_static/releases/test/index.html

# Create or recreate a symbolic link
rm -f /data/web_static/current
ln -s /data/web_static/releases/test/ /data/web_static/current

# Give ownership to the ubuntu user and group recursively
chown -R ubuntu:ubuntu /data/

# Update Nginx configuration
config_file="/etc/nginx/sites-available/default"
if grep -q 'location /hbnb_static {' "$config_file"; then
    sed -i '/location \/hbnb_static {/!b;n;c alias /data/web_static/current/;' "$config_file"
else
    sed -i '/server_name _;/a location /hbnb_static {\n alias /data/web_static/current/;\n}' "$config_file"
fi

# Restart Nginx
service nginx restart
