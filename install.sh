#!/bin/bash

echo " ------  Update package index"
apt-get update -y

echo " ------  Installing pip3"
apt-get install python3-pip -y

echo " ------  Installing python3-openssl"
apt-get install python3-openssl -y

echo " ------  Installing git "
apt-get install  git   -y

echo " ------  Cloning git project repo"
cd / ; git clone https://github.com/KamilBabayev/Cisco.git /var/www/html

mkdir /db ;  mv /var/www/html/webapp/users.db /db  ; chown -R www-data:www-data /db/

echo " -----    Creating soft app.py  link"
ln -s /var/www/html/webapp/server.py  /var/www/html/webapp/app.py


echo " ------  Installing nginx uwsgi"
apt-get install uwsgi-plugin-python3

echo " ------  Upgrading pip3"
pip3 install --upgrade pip

echo " ------  Installing paramiko"
pip3 install paramiko

echo " ------  Installing netmiko"
pip3 install netmiko

echo " ------  Installing flask"
pip3 install flask

echo " ------  Installing flask alchemy orm etxension"
pip3 install flask_sqlalchemy

echo " ------  Installing flask Form extension"
pip3 install flask_wtf

echo " ------  Installing Nginx Uwsgi"
apt-get install nginx -y
apt-get install uwsgi -y


rm -rf /etc/nginx/sites-available/default ; /etc/nginx/sites-enabled/default

wget https://raw.githubusercontent.com/KamilBabayev/Cisco/master/nginx_cisco.conf -O  /etc/nginx/sites-available/cisco_nginx.conf

ln -s /etc/nginx/sites-available/cisco_nginx.conf  /etc/nginx/sites-enabled/

wget https://raw.githubusercontent.com/KamilBabayev/Cisco/master/cisco.ini -O /etc/uwsgi/apps-available/cisco.ini

ln -s /etc/uwsgi/apps-available/cisco.ini /etc/uwsgi/apps-enabled/cisco.ini

/etc/init.d/nginx   restart ; /etc/init.d/uwsgi  restart





