FROM php:7.4-apache

# Create the flag directory and file
RUN mkdir -p /flag
RUN echo "flag-arbyci" > /flag/flag.txt

# Copy source code to web root
COPY src/ /var/www/html/

# Expose port 80
EXPOSE 80
