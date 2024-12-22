#!/bin/bash
set -e

# Initialize the database if necessary
if [ ! -d "/db/mysql" ]; then
  echo "Initializing MariaDB data directory..."
  mysql_install_db --user=mysql --datadir=/db
fi

# Start MariaDB in the background
mysqld_safe --datadir=/db &

# Wait for MariaDB to start
sleep 5

# Check if the database exists, if not, create it
if ! mysql -u root -p"pinyator" -e "USE pinyator"; then
  echo "Creating database pinyator..."
  mysql -u root -p"pinyator" -e "CREATE DATABASE IF NOT EXISTS pinyator;"
  mysql -u root -p"pinyator" -e "GRANT ALL PRIVILEGES ON pinyator.* TO 'pinyator'@'localhost' IDENTIFIED BY 'pinyator';"
  echo "Loading initial data..."
  mysql -u root -p"pinyator" 'pinyator' </var/www/html/pinyator/Pinyator_BD.sql
fi

# Start Apache in the foreground
exec apache2-foregrounSELECT user,authentication_string,plugin,host FROM mysql.user
