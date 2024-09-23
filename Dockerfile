# Use the official PHP image with MySQL support
FROM php:7.2-apache

# Install required PHP extensions and git
RUN apt-get update && apt-get install -y git \
    && docker-php-ext-install mysqli

# Clone the Pinyator repository from GitLab
RUN git clone https://gitlab.com/elputorei/Pinyator /var/www/html/pinyator

# Set the working directory
WORKDIR /var/www/html

# Change ownership to www-data and set appropriate permissions
RUN chown -R www-data:www-data /var/www/html/pinyator \
    && chmod -R 755 /var/www/html/pinyator

# Open port 80 to access the application
EXPOSE 80

