# Backend-Software-Engineer-CC-HEB

Using Flask to build a Python HTTP REST API.

Integrations with Flask-SQLalchemy.

## Installation

Clone this repository:

```
$ git clone git@github.com:fr4nkR/Backend-Software-Engineer-CC-HEB.git
```

From the directory from which this repo was cloned, go into the root directory for Backend-Software-Engineer-CC-HEB:

```
$ cd Backend-Software-Engineer-CC-HEB
```

Install with pip:

```
$ pip install -r requirements.txt
```

Create a .env file in the root directory of the flask application to specify the different secrets and configurations needed needed:
```
$ touch .env
```

Inside .env file:

```
SQLALCHEMY_DATABASE_URI='postgresql://user:password@localhost/somedb'
SQLALCHEMY_ECHO='False'
SQLALCHEMY_TRACK_MODIFICATIONS='False'
FLASK_DEBUG = 'False'
```

## Flask Application Structure 
```
.
|──────app/
| |────__init__.py
| |────routes.py
| |────models.py
| |────helpers.py
|──────.env
|──────.gitignore
|──────requirements.txt
|──────config.py
|──────run.py
|──────README.md

```

## Run API:

### Run flask 
```
$ python3 run.py
```

The default port is 5000. Unless specified otherwise, this API will run locally:

`http://127.0.0.1:5000/customers`

or

`http://localhost:5000/customers`