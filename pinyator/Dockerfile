# Use an official PHP runtime as a parent image
FROM php:8.2-apache

# Set build arguments for repository URL
ARG REPO_URL=https://github.com/guillemglez/Pinyator

# Install system dependencies and MariaDB
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    mariadb-server \
    && docker-php-ext-install mysqli pdo pdo_mysql \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Enable mod_rewrite for Apache
RUN a2enmod rewrite

# Set environment variables from .env
ENV MYSQL_ROOT_PASSWORD=${MYSQL_ROOT_PASSWORD}
ENV MYSQL_USER=${MYSQL_USER}
ENV MYSQL_PASSWORD=${MYSQL_PASSWORD}
ENV MYSQL_DATABASE=${MYSQL_DATABASE}

# Create the /db directory and set appropriate permissions
RUN mkdir -p /db && chown -R mysql:mysql /db

# Configure MariaDB to use the /db directory for storage
RUN sed -i 's|datadir.*|datadir = /db|' /etc/mysql/mariadb.conf.d/50-server.cnf

# Prevent MariaDB from trying to start during the Docker build process
RUN echo '[mysqld]' > /etc/mysql/my.cnf \
    && echo 'skip-host-cache' >> /etc/mysql/my.cnf \
    && echo 'skip-name-resolve' >> /etc/mysql/my.cnf \
    && echo 'skip-networking' >> /etc/mysql/my.cnf \
    && echo 'skip-slave-start' >> /etc/mysql/my.cnf

# Clone the repository into the container
RUN git clone ${REPO_URL} /var/www/html/pinyator

# Modify the Connexio.php file to use environment variables
RUN sed -i "s/'user'/'${MYSQL_USER}'/" /var/www/html/pinyator/Connexio.php \
    && sed -i "s/'password'/'${MYSQL_PASSWORD}'/" /var/www/html/pinyator/Connexio.php \
    && sed -i "s/'pinyator'/'${MYSQL_DATABASE}'/" /var/www/html/pinyator/Connexio.php

# Set the working directory
WORKDIR /var/www/html/pinyator

# Copy the entrypoint script
COPY entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/entrypoint.sh

# Use the entrypoint script
ENTRYPOINT ["entrypoint.sh"]

# Expose port 80 for the application
EXPOSE 80

# Health check for the server
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD curl -f http://localhost/pinyator/Index.php || exit 1
