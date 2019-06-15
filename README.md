# Aper Backend

Aper backend is a small API coded for the Banque Portonal Hackathon.

## Installation

Make sure you have Python 3.x and Pipenv installed. Clone this project and, from the cloned directory, run the commands below to get started.

You will need:

- A SQLite database
- A Google Auth client id: https://developers.google.com/identity/sign-in/web/sign-in

Start by configuring your own local instance of the project:

```
mkdir instance
touch instance/config.py
```

Be sure to set the following parameters in the file you just created:

- ENV: set it to 'development' in your local machine
- SECRET_KEY: so your app does not get hacked (too easily)
- GOOGLE_CLIENT_ID: what you just got from google
- SQLALCHEMY_DATABASE_URI: URI to your database

Having done that, we can install the app:

```
pipenv install
pipenv shell
export FLASK_APP=aper
flask db upgrade
python run.py
```
