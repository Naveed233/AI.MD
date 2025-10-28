FROM php:8.1-cli

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    libonig-dev \
    libxml2-dev \
    && docker-php-ext-install pdo pdo_mysql mbstring \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Composer
COPY --from=composer:latest /usr/bin/composer /usr/bin/composer

WORKDIR /var/www/html

# Copy composer file only
COPY composer.json ./

# Install dependencies without lock file
RUN composer install --no-dev --ignore-platform-reqs || true

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Start server
CMD ["php", "-S", "0.0.0.0:8000", "-t", "."]
