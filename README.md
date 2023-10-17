# SEP30


##Overview
Welcome to the Mental Health Dashboard project repository! This repository contains all the files and resources related to our innovative Mental Health Dashboard powered by Twitter data. Our dashboard provides valuable insights and analysis related to mental health discussions on Twitter, helping users understand trends, sentiments, and demographics surrounding mental health topics.

##Project Description
The Mental Health Dashboard project aims to provide users with a comprehensive tool for understanding, analyzing, and improving mental well-being based on Twitter data. By processing and analyzing tweets, the dashboard offers real-time insights into mental health discussions, including sentiment analysis, demographic breakdowns, and topic modeling.

##Features
1. Real-Time Analysis: Stay updated with live mental health trends on Twitter.
2. Sentiment Analysis: Gauge the overall sentiment of mental health discussions.
3. Demographic Insights: Understand how different demographics perceive mental health.
4. Topic Modeling: Explore interconnected mental health topics.
5. Keyword Distribution: Identify prevalent mental health keywords.
6. Location Demographics: Visualize mental health discussions across different regions.
7. Interactive Dashboard: User-friendly interface allowing users to tailor searches and explore data easily.

## Frontend

In order to locally run project, you will need to:

1. Clone this project:

   `git clone git@github.com:morganrmcconnon/SEP30.git`

2. Nagivate to frontend folder and install required dependencies:
   
   `cd frontend`
   
   `npm install`

4. Run dev environment:

   `npm run dev`

## Backend

### Installation and run

Run the following command to start the app:
```bash
flask --app app.py run
```
or

```bash
flask run
```
(this command will automatically run the Flask application since we named the main python file as `app.py`)

or

```bash
python app.py
```

### Development

#### Auto genereate `requirements.txt`

To auto generate `requirements.txt` file, run the following command while in the virtual environment:

```bash
pip freeze > requirements.txt
```

##Usage
To use the Mental Health Dashboard, open your web browser and access the provided URL after starting the application. Explore various features and insights related to mental health discussions on Twitter.

##Technologies Used
1. Frontend: React.js, HTML, CSS, JavaScript
2. Backend: Python, Flask, MongoDB
3. Other Tools: Git


## Prototype sketch

[Figma Prototype](https://www.figma.com/file/ScVgs5wpsr3FTM7npCqg1n/Dashy-Dashboard-(Community)?type=design&node-id=302-925)

![Dashboard Prototype](https://i.imgur.com/avDdZkH.png)

##Contact
For any inquiries or feedback, please contact us at twittermentalhealth30@gmail.com.

Thank you for using the Mental Health Dashboard! Together, let's create awareness and understanding around mental health discussions on social media. Happy exploring!
