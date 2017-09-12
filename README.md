# Crisis Management Office

Project for CZ3003 Software System Analysis and Design, group SSP3.

## Getting Started Guide

### Getting Started for macOS and Unix-like

To run the server for this project, we will do the following:

1. Install `pip`
2. Install `virtualenv` and activate it
3. Install all python dependecies for this project
4. Run the server

First, we will install pip by following installation guide at 
https://pip.pypa.io/en/stable/installing/

```shell
$ curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
$ python get-pip.py
```

Next, we will install `virtualenv` using `pip`, create a virtual environment, and activate the 
environment. 

```shell
$ sudo python -m pip install virtualenv
$ virtualenv cmoenv
$ source cmoenv/bin/activate
```

Next, we will install all requirements/dependencies for this project using `pip`.

```
$ pip install -r requirements.txt
```

Finally, we start the server using the followin command:

```shell
# Make sure you are in <root>/src folder before running the server
$ cd src/

# Create Table in SQLite database.
$ python manage.py migrate

# Run the server.
# The website can be accessed at http://localhost:8080
$ python manage.py runserver
```

At the end of our development, we call `deactivate` in command line to deactivate `virtualenv`.

We don't install these dependecies everytime when we want to develop for this project. A normal 
workflow would be:

```shell
$ source cmoenv/bin/activate

$ cd src/
$ python manage.py runserver

# When you are done
$ deactivate
```

### Getting Started using Docker

This option would allow any platforms that are supported by Docker to build and run this project.
In addition, a MySQL backend will be used to store data, instead of SQLite.

First, we need to install Docker from https://www.docker.com/. Then, run the following commands:

```shell
# Run the server.
# The website can be accessed at http://localhost:80
$ docker-compose up

# Create Table in MySQL server
$ docker exec -it cz3003ssp3cmo_cmo_1 python manage.py migrate --settings cmo.prod_settings

# Create admin user
$ docker exec -it cz3003ssp3cmo_cmo_1 python manage.py createsuperuser --settings cmo.prod_settings
```

Both the server for this project and the MySQL server will be runned. All data in MySQL server will
be stored at `./mysql/tmp/` folder. Few useful commands to work with the MySQL server using Docker:

```shell
# Get the name of the CMO DB by running docker command, and set the name to a variable
$ docker ps
$ DOCKER_CMO_DB_NAME=cz3003ssp3cmo_db_1
$ DOCKER_CMO_NAME=cz3003ssp3cmo_cmo_1

# Execute some sql commands in the mysql server
$ docker exec -i $DOCKER_CMO_DB_NAME mysql -uroot -pcmodb  <<< "use cmodb; select database();"

# Dump all databases to command line outputs
$ docker exec cz3003ssp3cmo_db_1 sh -c 'exec mysqldump --all-databases -uroot -p"cmodb"'
```

## Linter and Formatter

We follow pep8 style guide for python.

To lint our codes:

```shell
$ pip install pylint
$ find src -iname "*.py" | xargs pylint
```

To format our codes:

```shell
$ pip install yapf
$ find src -iname "*.py" | xargs yapf -i
```
