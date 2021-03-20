# Likers Social network

Where users can like other users posts!

## Prerequisites

Install requirements and create virtual environment

    poetry install

If running without Docker - create PostgreSQL database, specify your own DB name, username, password.
Just don't forget to set it in environment variables later.

    create database likers;
    create user likers_user with encrypted password 'likers_pass';
    grant all privileges on database likers to likers_user;
    alter user likers_user createdb;

Migrate

    python manage.py migrate

## Run

### Docker
Set environment variables as in `.env.example`.

Execute

    docker-compose up

### Local
Adjust environment variables in `.env`.

Execute

    python manage.py 0.0.0.0:8000

Assuming you have RabbitMQ up and running. To start celery run

    celery -A src.celery:app worker -l info -B

## Usage

API is documented via Swagger at [/swagger](http://127.0.0.1:8000/swagger/)

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