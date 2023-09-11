# 1. Install nginx, git, python3, pip3

# Update apt
sudo apt update -y

# Install nginx
sudo apt install nginx-core -y

# # Install git
# sudo apt install git -y

# # Install python3
# sudo apt install python3 -y

# Install pip3
sudo apt install python3-pip -y


# 2. Prepare the server


# Make sure to navigate to the home directory before running this script
cd ~


# 2. - Clone the repo and pull the latest changes


# Clone the repo
git clone https://github.com/morganrmcconnon/SEP30.git

# Pull the latest changes
cd ~/SEP30
git pull


# 2. - Configure nginx


# Copy the nginx config file
sudo cp ~/SEP30/nginx/ubuntu/default /etc/nginx/sites-available/default


# 2. - Configure the frontend


# Copy the dist folder from your local machine to /home/ubuntu/SEP30/frontend
# Use WinSCP if you're on Windows
# Or use scp
# scp -r ~/Desktop/SEP30/frontend/dist ubuntu@<ip-address>:/home/ubuntu/SEP30/frontend

# Copy the dist folder to the nginx root
sudo cp -r ~/SEP30/frontend/dist/* /var/www/html/


# 2. - Configure the backend


# Navigate to the backend directory
cd ~/SEP30/backend

# Install the requirements
pip install -r requirements.txt



# 3. Start the web server


# 3. - Frontend


# Start nginx
sudo systemctl start nginx

# Or restart nginx
sudo systemctl restart nginx

# Check the status of nginx
sudo systemctl status nginx

# Stop nginx
sudo systemctl stop nginx


# 3. - Backend


# Start a tmux session called backend
# so the backend can run in the background after you exit the ssh session
tmux new -s backend

# Navigate to the backend directory
cd ~/SEP30/backend

# Run the backend
python3 wsgi.py &
# Or you can run the backend with gunicorn

# End tmux session if you want to
tmux kill-session -t backend


# 4. Install MongoDB


# Reference: https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-ubuntu/

# From a terminal, install gnupg and curl if they are not already available:
sudo apt-get install gnupg curl

# To import the MongoDB public GPG key from https://pgp.mongodb.com/server-7.0.asc, run the following command:
curl -fsSL https://pgp.mongodb.com/server-7.0.asc | \
   sudo gpg -o /usr/share/keyrings/mongodb-server-7.0.gpg \
   --dearmor

# Create a list file for MongoDB
echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-7.0.gpg ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/7.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-7.0.list

# Reload local package database
sudo apt-get update

# Install the MongoDB packages
sudo apt-get install -y mongodb-org

# Start MongoDB
sudo systemctl start mongod

# Verify that MongoDB has started successfully
sudo systemctl status mongod

# Stop MongoDB
sudo systemctl stop mongod

# Restart MongoDB
sudo systemctl restart mongod



# 5. Use MongoDB


# Begin using MongoDB
mongosh


# Create or switch to the 'twitter_db' database
use twitter_db;

# Create 'original_tweets' collection
db.createCollection('original_tweets');

# Create 'analyzed_tweets' collection
db.createCollection('analyzed_tweets');

# Create 'analyzed_users' collection
db.createCollection('analyzed_users');

# Show collections
show collections;

# Show databases
show dbs;

# Exit mongosh
exit;
