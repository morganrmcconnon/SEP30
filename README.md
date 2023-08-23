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

Refer to https://flask.palletsprojects.com/en/2.3.x/installation/.

To run the backend app, first navigate to the back-end folder, create a virtual environment, activate it, and install the dependencies.

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

(Note that at the moment requirements.txt does not record every Python library used for this project yet, so make sure that all libraries has been pip installed in the virtual environment. To install a library with pip in the virtual environment just simply run `pip install <library>`

If you have already done the installation processes and are prepared to run the app then:

If not already, enable the virtual environment:
```bash
.venv\Scripts\activate
```

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
