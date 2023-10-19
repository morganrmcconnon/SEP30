# SEP30 - Mental Health Dashboard

## Technologies used

### Frontend
- Web framework: React.js
- Languages: TypeScript, JavaScript, HTML, CSS
- Tools: Node, npm, Vite, 

### Backend
- Web framework (API): Flask
- Languages: Python
- Tools: pip

### Database
- MongoDB

## System Architecture description

Our system consists of a data warehouse, a data analysis server side application, an API, and a frontend web application.

- In the backend, we have a list of **Python components** that are Python modules that provide the ability to collect, process, and analyse data from Twitter. These modules are used by the **data analysis server side application** to collect, process, and analyse data from Twitter, and by the **API** to expose those functions to the **frontend**. In this document, we will refer to these modules as **Python components** or **components**. 

- The **data analysis server side application** is responsible for collecting, processing, and analysing data from Twitter. For this document, we will refer to this application as the **analysis pipeline**.

- The **data warehouse** is responsible for storing the collected data, processed data, and analysis results by the **analysis pipeline**. For our project, we are using a MongoDB database called `twitter_db` as our data warehouse. We will refer to this database as the **data warehouse** or **database** in this document.

- The **API** is responsible for providing the frontend web application with the processed data from the **data warehouse**, and the analysis functions provided by the **Python components**. In this document, we will refer to this application as the **API**.

- All the **Python components**, the **analysis pipeline**, and the **API** are stored in the `backend` folder.

- The **frontend web application** is responsible for displaying the **dashboard**. The **dashboard** is a **web application** that provides users with various visualisations, insights and analysis results related to mental health discussions on Twitter. In this document, we will refer to this application as the **frontend**.

- The **frontend** is stored in the `frontend` folder.

## Local installation and deployment in a development environment

### Pre-requisites

- Operating system: Windows 10/11 or Ubuntu 22.04.
- Internet connection.
- Node.js. Recommended version: Node v20.7.0
- Python 3. Recommended version: Python 3.11.5
- pip (Python package manager). Recommended version: pip 23.2.1
- MongoDB. Recommended version: v7.0.0

### Dependencies

#### Frontend's Node modules

- **Node modules**: A list of all the Node modules used in this project can be found in the `package.json` and `package-lock.json` file in the `frontend` folder.

#### Backend's Python packages

A list of all the neccessary Python packages used in this project can be found in the `requirements.txt` file in the `backend` folder. 

In the `backend` folder, we also have a `requirements-full-ubuntu.txt` file for all Python packages needed specifically for Ubuntu 22.04, and a `requirements-full-windows.txt` file for all Python packages needed specifically for Windows 10/11.

### Setup

#### Download the source code

To setup the project, you will need to download this repository, i.e. the source code of this project.

You can clone this repository using the following command:

```bash
git clone git@github.com:morganrmcconnon/SEP30.git
```

#### Install frontend dependencies

Nagivate to frontend folder and install the required node dependencies:
```bash
cd frontend
npm install
```

#### Install backend dependencies

Nagivate to backend folder and install required dependencies from the `requirements.txt` file:
```bash
cd backend
pip install -r requirements.txt
```

You can also choose to install all the dependencies from the `requirements-full-ubuntu.txt` file if you are using Ubuntu 22.04, or from the `requirements-full-windows.txt` file if you are using Windows 10/11.

### Deployment of the dashboard

To deploy the dashboard, you will only need to start the **frontend**, and the **API**. You may also need to start MongoDB so that the dashboard can collect data from the database, however the current implementation is set up so that you don't need to start MongoDB. The API will instead send data from a cached file called `backend/cache/backend_response.json`. 

In addition, you will also need to start the analysis pipeline to collect, process, and analyse Twitter data.

#### Frontend

Run the following command to start the frontend app:
```bash
npm run dev
```

#### API

Run the following command to start the API:
```bash
flask --app app.py run
```
or
```bash
flask run 
```
(this command will automatically run the Flask API application since we named the main python file as `app.py`)

### Deployment of the analysis pipeline

#### MongoDB

To run the analysis pipeline, you will first need to start MongoDB so that the **analysis pipeline** can store the collected data, processed data, and analysis results in the database. 

Run the following command to start MongoDB:

```bash
# On Ubuntu:
sudo systemctl start mongod
```

#### Analysis pipeline

Run the following command to start the **analysis pipeline**:

```bash
# On Windows:
python populate_data.py
# On Ubuntu:
python3 populate_data.py
```

The `populate_data.py` script is a CLI that will use the `components/pipeline.py` module to start collecting, processing, and analysing Twitter data from the Internet Archive's Twitter Stream Collection on October 15th, 2022 at 12:00 pm.

Optionally, you can also run the following command to start the `populate_data.py` script to download data from a specific date, and/or to download data on loop from a starting date forward/backward a specific time. For example, to download data from October 9th, 2022, at 16:30 pm, looping from that date, forward, in an interval of 1 day, 2 hours, and 3 minues, run the following command:

```bash
python populate_data.py -d 9 -m 10 -y 2022 -H 0 -M 0 -dd 1 -dH 2 -dM 3 -l -f
```

### Development

\[TBC\]

### Auto genereate `requirements.txt`

To auto generate `requirements.txt` file, run the following command while in the Python virtual environment:

```bash
pip freeze > requirements.txt
```

## Deployment in a production environment

### Pre-requisites

All the pre-requisites and dependencies for the development environment are also required for the production environment.

In addition, you will also need to install the following:

- A web server that can also be used as a reverse proxy, load balancer, mail proxy and HTTP cache. We will use this web server as a reverse proxy to serve the frontend and the API. For this document, we will use **Nginx**.

- A Python WSGI HTTP Server for serving the Flask **API**. Recommended: **Gunicorn** (if not Windows) or **Waitress** (if on Windows). We have written a `server.py` file in the `backend` folder that will serve the Flask application using **Waitress**. You can use this file to serve the Flask application using a WSGI HTTP Server.

### Setup

#### Nginx

First, download and install Nginx.

Then, configure Nginx to proxy all request to endpoints starting with `/api/` or `/backend/` to port 5000 (127.0.0.1:5000).

i.e. configure and add the following to the nginx configuration file (for Windows, it is `nginx.conf`, for Ubuntu, it is `/etc/nginx/sites-available/default`):

```
# proxy the API requests to the Flask server listening on port 5000
location /api/ {
   proxy_pass http://127.0.0.1:5000/api/;
}

# proxy the API requests to the Flask server listening on port 5000
location /backend/ {
   proxy_pass http://127.0.0.1:5000/backend/;
}
```

### Deployment of the dashboard

Similar to the development environment, to deploy the dashboard, you will only need to start the **frontend**, and the **API**. You may also need to start MongoDB so that the dashboard can collect data from the database, however the current implementation is set up so that you don't need to start MongoDB. The API will instead send data from a cached file called `backend/cache/backend_response.json`.

#### Frontend

To deploy the frontend, you will need to build the frontend app and serve the built app using a web server.

Run the following command to build the frontend app:

```bash
npm run build
```

This will create a `dist` folder in the `frontend` folder. You can then serve the `dist` folder using the web server.

#### API

To deploy the API, you will need to serve the Flask application using a WSGI HTTP Server.

We have written a `server.py` file in the `backend` folder that will serve the Flask application. You can use this file to serve the Flask application using a WSGI HTTP Server.

Run the following command to serve the Flask application using the `server.py` file:

```bash
python server.py
```

### Deployment of the analysis pipeline

Deploying the analysis pipeline is the same as deploying the analysis pipeline in the development environment.

## Project description

### Overview
Welcome to the Mental Health Dashboard project repository! This repository contains all the files and resources related to our innovative Mental Health Dashboard powered by Twitter data. Our dashboard provides valuable insights and analysis related to mental health discussions on Twitter, helping users understand trends, sentiments, and demographics surrounding mental health topics.

### Project Description
The Mental Health Dashboard project aims to provide users with a comprehensive tool for understanding, analyzing, and improving mental well-being based on Twitter data. By processing and analyzing tweets, the dashboard offers real-time insights into mental health discussions, including sentiment analysis, demographic breakdowns, and topic modeling.

### Features
1. Real-Time Analysis: Stay updated with live mental health trends on Twitter.
2. Sentiment Analysis: Gauge the overall sentiment of mental health discussions.
3. Demographic Insights: Understand how different demographics perceive mental health.
4. Topic Modeling: Explore interconnected mental health topics.
5. Keyword Distribution: Identify prevalent mental health keywords.
6. Location Demographics: Visualize mental health discussions across different regions.
7. Interactive Dashboard: User-friendly interface allowing users to tailor searches and explore data easily.

### Usage
To use the Mental Health Dashboard, open your web browser and access the provided URL after starting the application. Explore various features and insights related to mental health discussions on Twitter.

### Technologies Used
1. Frontend: React.js, HTML, CSS, JavaScript
2. Backend: Python, Flask, MongoDB
3. Other Tools: Git


### Prototype sketch

[Figma Prototype](https://www.figma.com/file/ScVgs5wpsr3FTM7npCqg1n/Dashy-Dashboard-(Community)?type=design&node-id=302-925)

![Dashboard Prototype](https://i.imgur.com/avDdZkH.png)

### Contact
For any inquiries or feedback, please contact us at twittermentalhealth30@gmail.com.

Thank you for using the Mental Health Dashboard! Together, let's create awareness and understanding around mental health discussions on social media. Happy exploring!
