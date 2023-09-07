# 101-setup_web_static.pp
# Configures a web server for deployment of web_static.

# Ensure Nginx configuration
$nginx_conf = "server {
    listen 80 default_server;
    listen [::]:80 default_server;
    add_header X-Served-By ${hostname};
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
}"

package { 'nginx':
  ensure   => 'present',
  provider => 'apt'
} ->

file { '/data':
  ensure  => 'directory',
  owner   => 'ubuntu',
  group   => 'ubuntu',
  recurse => true
} ->

file { '/data/web_static':
  ensure => 'directory',
  owner  => 'ubuntu',
  group  => 'ubuntu'
} ->

file { '/data/web_static/releases':
  ensure => 'directory',
  owner  => 'ubuntu',
  group  => 'ubuntu'
} ->

file { '/data/web_static/releases/test':
  ensure => 'directory',
  owner  => 'ubuntu',
  group  => 'ubuntu'
} ->

file { '/data/web_static/shared':
  ensure => 'directory',
  owner  => 'ubuntu',
  group  => 'ubuntu'
} ->

file { '/data/web_static/releases/test/index.html':
  ensure  => 'present',
  content => "Holberton School Puppet\n",
  owner   => 'ubuntu',
  group   => 'ubuntu'
} ->

file { '/data/web_static/current':
  ensure => 'link',
  target => '/data/web_static/releases/test',
  owner  => 'ubuntu',
  group  => 'ubuntu'
} ->

exec { 'chown -R ubuntu:ubuntu /data/':
  path => '/usr/bin/:/usr/local/bin/:/bin/'
}

file { '/var/www':
  ensure => 'directory'
} ->

file { '/var/www/html':
  ensure => 'directory'
} ->

file { '/var/www/html/index.html':
  ensure  => 'present',
  content => "Holberton School Nginx\n"
} ->

file { '/var/www/html/404.html':
  ensure  => 'present',
  content => "Ceci n'est pas une page\n"
} ->

file { '/etc/nginx/sites-available/default':
  ensure  => 'present',
  content => $nginx_conf
} ->

exec { 'systemctl restart nginx':
  path => '/usr/bin/:/usr/local/bin/:/bin/'
}
