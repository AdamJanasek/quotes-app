# It's simple flask app integrated with FavQs API v2.
API docs are available at https://favqs.com/api.
## Installation
Create virtual environment for python, according to this source:  
##### https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/.  
Install with pip:
```
$ pip install -r requirements.txt
```
Set .env file:
```
FLASK_ENV=development
SECRET_KEY=YOUR_OWN_SECRET_KEY
API_KEY=API_KEY
API_URL=https://favqs.com/api/
```
To obtain API Key you need visit https://favqs.com/api and sign up.
## Run app
```
flask run
```
The application runs on port 5000.
It is available at http://localhost:5000/.
