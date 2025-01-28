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

COPY ./docker/my.cnf /etc/mysql/my.cnf

# Clone the repository into the container
COPY ./pinyator /var/www/html/pinyator

# Set the working directory
WORKDIR /var/www/html/pinyator

# Copy the entrypoint script
COPY docker/entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/entrypoint.sh

# Use the entrypoint script
ENTRYPOINT ["entrypoint.sh"]

# Expose port 80 for the application
EXPOSE 80

# Health check for the server
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD curl -f http://localhost/pinyator/Index.php || exit 1
