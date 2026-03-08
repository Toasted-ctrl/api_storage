# API Storage
Hi! This is a practise project where I wanted to try out creating an API that could facilitate storing raw json responses from another tool directly in a database.
## Why?
I'm mainly doing this as I wanted to learn about running an application through Docker, as well as trying to create a scalable API. I also wanted to learn about NGINX to make this an API that I could load-balance if needed.
## What does it do?
In this tool I also wanted to cover management functions, such as authentication through an API key (stored as a hash in the database), as well as user management if you're an admin. Additionally it provides some features to interact with the data we've stored in the 'ingest' table. The API is built on the FastAPI library.
## Tech stack
- PostgreSQL
- SQLAlchemy
- FastAPI
- Docker
- Pydantic