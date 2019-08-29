# Likers Social network
Where users can like other users posts!

Written in Python 3.

## Prerequisites

Create virtual environment and install requirements

    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt

Create PostgreSQL database, specify your own DB name, username, password, just don't forget to set it in environment
variables later.
    
    create database likers;
    create user likers_user with encrypted password 'likers_pass';
    grant all privileges on database likers to likers_user;
    alter user likers_user createdb;

Migrate
    
    python manage.py migrate

## Run

Specify environment variables:

    DEBUG=True/defaul is False
    SITE_IP=*/or something specific
    # DB params, if not as in settings.py
    DB_HOST
    DB_PORT
    DB_NAME
    DB_USER
    DB_PASSWORD

