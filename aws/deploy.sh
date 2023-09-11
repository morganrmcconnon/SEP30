# Copy the dist folder from your local machine to /home/ubuntu/SEP30/frontend
scp -i "path/to/your-key-pair-file.pem" -r "path/to/dist/*" ubuntu@ec2-ip-address.compute-1.amazonaws.com

# SSH into the EC2 instance
ssh -i "path/to/your-key-pair-file.pem" ubuntu@ec2-ip-address.compute-1.amazonaws.com

# Copy the dist folder to the nginx root
sudo cp -r ~/SEP30/frontend/dist/* /var/www/html/

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
