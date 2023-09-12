# Build the frontend
cd /path/to/frontend
npm run build

# SSH into the EC2 instance
ssh -i "path/to/your-key-pair-file.pem" ubuntu@ec2-ip-address.compute-1.amazonaws.com

# Remove the contents of the nginx root
sudo rm -rf /var/www/html/*

# Remove the dist folder
sudo rm -rf ~/SEP30/frontend/dist

# Exit the ssh session and go back to your local machine
exit

# Copy the dist folder from your local machine to /home/ubuntu/SEP30/frontend
scp -i "path/to/your-key-pair-file.pem" -r "path/to/dist/*" ubuntu@ec2-ip-address.compute-1.amazonaws.com:~/SEP30/frontend/

# SSH into the EC2 instance
ssh -i "path/to/your-key-pair-file.pem" ubuntu@ec2-ip-address.compute-1.amazonaws.com

# Copy the dist folder to the nginx root
sudo cp -r ~/SEP30/frontend/dist/* /var/www/html/

# Start nginx
sudo systemctl start nginx

# Or restart nginx
sudo systemctl restart nginx

# Git pull
cd ~/SEP30
git pull

# Navigate to the backend directory
cd ~/SEP30/backend

# Install the requirements if requirements.txt has changed
pip install -r requirements.txt

# Start a tmux session called backend
# so the backend can run in the background after you exit the ssh session
tmux new -s backend

# Start the backend
python3 wsgi.py
