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
    # Clearbit API Key
    CLEARBIT_KEY

## Bot
Adjust `src.bot.settings` as you like, it is self-explanatory.

To run automated bot, showing how this API works, run

    python run_bot.py

Bot makes following steps, logging useful information:

  - Signup number of users, provided in config
  - Get access token for each user
  - Each user creates random number of posts, up to max number provided in config, with random text
  - Like posts by following rules:
    - Next user to like a post is the one with most posts
    - User can like posts from users who have at least one post with 0 likes
    - User can't like own posts or single post twice
    - User likes posts until reaches max likes count, provided in config
    - Bot stops if every post has at least one like