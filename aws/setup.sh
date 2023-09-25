# 1. Install node, python3.11, pip3, git, mongodb, nginx

# Update apt
sudo apt update -y

# Update apt-get
sudo apt-get update -y

# Install nvm
# Reference: https://github.com/nvm-sh/nvm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.5/install.sh | bash

# Install node latest version
nvm install node

# # Install git
# sudo apt install git -y

# # Install python3
# sudo apt install python3 -y

# Install python3.11 in case the default python3 is lower than 3.11 (e.g. 3.10)
# Reference: https://www.itsupportwale.com/blog/how-to-upgrade-to-python-3-11-on-ubuntu-20-04-and-22-04-lts/
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt-get update
apt-get update
apt list | grep python3.11
sudo apt-get install python3.11
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.10 1
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 2
sudo update-alternatives --config python3
2
python3 -V

# Install pip3
sudo apt install python3-pip -y

# Upgrade pip3
pip3 install --upgrade pip


# Install nginx
sudo apt install nginx-core -y


# Install mongodb
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



# 2. Prepare the server


# Make sure to navigate to the home directory before running this script
cd ~


# 2. Clone the repo and pull the latest changes


# Clone the repo
git clone https://github.com/morganrmcconnon/SEP30.git

# Pull the latest changes
cd ~/SEP30
git pull


# 3. Configure nginx


# Copy the nginx config file
sudo cp ~/SEP30/nginx/ubuntu/default /etc/nginx/sites-available/default


# Copy the dist folder to the nginx root
sudo cp -r ~/SEP30/frontend/dist/* /var/www/html/


# 4. Configure the backend


# Navigate to the backend directory
cd ~/SEP30/backend

# Install the requirements
pip install -r requirements.txt


# Troubleshooting: Special case for Python.h not found and pip install hdbscan
# https://stackoverflow.com/questions/21530577/fatal-error-python-h-no-such-file-or-directory
# https://stackoverflow.com/questions/73171473/how-to-resolve-error-could-not-build-wheels-for-hdbscan-which-is-required-to-i
sudo apt-get install python3-dev
sudo apt-get install python3.11-dev
sudo apt install libpython3.11-dev
python3 -m pip install python-dev-tools --user --upgrade
pip3 install --upgrade pip
# (Seems that after upgrading pip, it is possible to install hdbscan)



# 5. Use mongo shell

# Use mongosh
mongosh

# Exit mongosh
exit;
