# Start the frontend, backend, and MongoDB


# 1. Start MongoDB

# Start MongoDB
sudo systemctl start mongod

# Verify that MongoDB has started successfully
sudo systemctl status mongod

# Stop MongoDB
sudo systemctl stop mongod

# Restart MongoDB
sudo systemctl restart mongod


# 2. Frontend

# Start nginx
sudo systemctl start nginx

# Or restart nginx
sudo systemctl restart nginx

# Check the status of nginx
sudo systemctl status nginx

# Stop nginx
sudo systemctl stop nginx


# 3. Backend

# Start a tmux session called 'backend' or whatever name you want
# so the backend can run in the background after you exit the ssh session
tmux new -s backend

# Navigate to the backend directory
cd ~/SEP30/backend

# Run the backend WSGI server
python3 wsgi.py &
# Or you can run the backend with gunicorn

# Run any script
python3 {script_name}.py

# End tmux session if you want to
tmux kill-session -t backend

