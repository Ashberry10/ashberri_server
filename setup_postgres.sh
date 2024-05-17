#!/bin/bash

# Variables
DB_NAME="ashberridb"
DB_USER="ashberri"
DB_PASS="123" # Consider using a more secure password

# Update system packages
echo "Updating system packages..."
apt update

# Install PostgreSQL and its contrib package
echo "Installing PostgreSQL..."
apt install -y postgresql postgresql-contrib

# Switch to the postgres user and create the database and user
echo "Creating database and user..."
sudo -u postgres psql -c "CREATE DATABASE $DB_NAME;"
sudo -u postgres psql -c "CREATE USER $DB_USER WITH PASSWORD '$DB_PASS';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;"

# Grant permissions to the user on the public schema
echo "Granting permissions to the user on the public schema..."
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON SCHEMA public TO $DB_USER;" $DB_NAME

# Modify pg_hba.conf for md5 authentication
PG_HBA_PATH=$(find /etc/postgresql -type f -name "pg_hba.conf")
echo "Configuring $PG_HBA_PATH for md5 authentication..."
sed -i "s/local   all             all                                     peer/local   all             all                                     md5/" $PG_HBA_PATH

# Modify postgresql.conf to listen on all interfaces
POSTGRESQL_CONF_PATH=$(find /etc/postgresql -type f -name "postgresql.conf")
echo "Configuring $POSTGRESQL_CONF_PATH to listen on all interfaces..."
sed -i "s/#listen_addresses = 'localhost'/listen_addresses = '*'/" $POSTGRESQL_CONF_PATH

# Restart PostgreSQL to apply changes
echo "Restarting PostgreSQL..."
systemctl restart postgresql

echo "PostgreSQL has been configured successfully."