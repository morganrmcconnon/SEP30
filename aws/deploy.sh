# SSH into the EC2 instance
ssh -i "path/to/your-key-pair-file.pem" ubuntu@ec2-ip-address.compute-1.amazonaws.com

# Git pull
cd ~/SEP30
git pull

# Navigate to the frontend directory
cd ~/SEP30/frontend

# Remove the contents of the nginx root
sudo rm -rf /var/www/html/*

# Remove the dist folder
sudo rm -rf ~/SEP30/frontend/dist

# Build the frontend to the dist folder (We are currently using 'Vite')
npm run build

# Copy the dist folder to the nginx root
sudo cp -r ~/SEP30/frontend/dist/* /var/www/html/


# Navigate to the backend directory
cd ~/SEP30/backend

# Install the requirements if requirements.txt has changed
pip install -r requirements.txt
