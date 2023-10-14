# SEP30

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


## Prototype sketch

[Figma Prototype](https://www.figma.com/file/ScVgs5wpsr3FTM7npCqg1n/Dashy-Dashboard-(Community)?type=design&node-id=302-925)

![Dashboard Prototype](https://i.imgur.com/avDdZkH.png)
