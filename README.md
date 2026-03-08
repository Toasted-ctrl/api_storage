# API Storage
Hi! This is a practise project where I wanted to try out creating an API that could facilitate storing raw json responses from another tool directly in a database.
## Why?
I'm mainly doing this as I wanted to learn about running an application through Docker, as well as trying to create a scalable API. I also wanted to learn about NGINX to make this an API that I could load-balance if needed. I also wanted to try build this including tests for everything. Previously, I mainly wrote stuff without tests, but in this project I wanted it to be more controlled, and follow best practises. My intention is to for now, only store the reponses. Any ETL processes to the data will be implemented in a separate application.
## What does it do?
In this tool I also wanted to cover management functions, such as authentication through an API key (stored as a hash in the database), as well as user management if you're an admin. Additionally it provides some features to interact with the data we've stored in the 'ingest' table. The API is built on the FastAPI library.
## Tech stack
- PostgreSQL
- SQLAlchemy
- FastAPI
- Docker
- Pydantic
## Requirements
### Database
You must already have a database instance running, including the following tables from the 'database.py' file:
- api_keys
- users
- ingest<br />
\You may generate these tables as well as add a system user without adding them manually to the database. Please see 'Initialize tables' to proceed.
### .env
The .env file must include:
- hostname
- password
- database
- user
- port
- db_type: i.e., 'postgresql' using this stack
- dbconnection: i.e., 'psycopg2' using this stack<br />
\The .env file must be added to the main directory.
### Initialize tables
To create all required tables without having to manually add them yourself, directly run app/init_database.py. Make sure that the .env file described is present. If you also wish to add a main admin user from the beginning, add the following to the .env file:
- "ApiKey_key_hashed" > a hashed api key (SHA256) for your main system user
- "User_first_name"
- "User_last_name"
- "User-email
## Tests
To run tests run pytest from the main directory, run "pytest -v" or "pytest --v". The test will create and discard an in-memory sqlite database, having a database with all tables presents already established is not required.
## Starting the API
To run the api, either create and run it as a docker container using the added Dockerfile, or run "uvicorn app.main:app --reload" from the main directory.