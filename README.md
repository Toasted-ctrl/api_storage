# DIA (Data Ingest API)
Hi! This is a practise project where I wanted to try out creating an API that could facilitate storing raw json responses from another tool directly in a database.
## Why?
I'm mainly doing this as I wanted to learn about running an application through Docker, as well as trying to create a scalable API. I also wanted to learn about nginx to make this an API that I could load-balance if needed. I also wanted to try build this including tests for everything. Previously, I mainly wrote stuff without tests, but in this project I wanted it to be more controlled, and follow best practises. My intention is to for now, only store the reponses. Any ETL processes to the data will be implemented in a separate application.
## What does it do?
In this tool I also wanted to cover management functions, such as authentication through an API key (stored as a hash in the database), as well as user management if you're an admin. Additionally it provides some features to interact with the data we've stored in the 'ingest' table. The API is built on the FastAPI library.
## Future updates
There is still some work left to do. I would like to:
- Expand on the type of data that may be ingested
## Tech stack
- PostgreSQL
- SQLAlchemy
- FastAPI
- Docker
- Pydantic
- Nginx
## Requirements
*Make sure to include 'src' in the pythonpath*. Run the below command from the main directory:
- Windows: $env:PYTHONPATH="src"
- Linux: export PYTHONPATH=$(pwd)/src
### Database
You must already have a database instance running, including the following tables from the 'src.database.schema' file. You may create these by running src/init_db directly. The .env file must contain all credentials and the database instance must be running when running src/init_db. The required tables are:
- api_keys
- users
- ingest
### .env
The database connection details must be present in the .env file. You will find an example .env file in the main directory. Rename to .env and enter your details. If you wish to add a main admin user when running src/init_db, set "include_admin_user" to "true" and add the user details.
## Tests
To run tests run pytest from the root directory, run "pytest -v" or "pytest -vv". *Do not forget to include 'src' into the pythonpath before running tests from the root directory.*
## Starting the API
To run the api, either build and run it as a set of docker containers (including load balancer through nginx) using the added docker compose file, or run "uvicorn main:app --reload" from the root directory. *Do not forget to include 'src' into the pythonpath if running from the root directory directly.*