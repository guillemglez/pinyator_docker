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
if ! mysql -u root -p"${MYSQL_ROOT_PASSWORD}" -e "USE ${MYSQL_DATABASE}"; then
    echo "Creating database ${MYSQL_DATABASE}..."
    mysql -u root -p"${MYSQL_ROOT_PASSWORD}" -e "CREATE DATABASE IF NOT EXISTS ${MYSQL_DATABASE};"
    mysql -u root -p"${MYSQL_ROOT_PASSWORD}" -e "GRANT ALL PRIVILEGES ON ${MYSQL_DATABASE}.* TO '${MYSQL_USER}'@'localhost' IDENTIFIED BY '${MYSQL_PASSWORD}';"
    echo "Loading initial data..."
    mysql -u root -p"${MYSQL_ROOT_PASSWORD}" ${MYSQL_DATABASE} </var/www/html/pinyator/Pinyator_BD.sql
fi

# Start Apache in the foreground
exec apache2-foreground
