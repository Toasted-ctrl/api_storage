import os
import psycopg2

from dotenv import load_dotenv
from fastapi import HTTPException

load_dotenv()

db_hostname = os.getenv("db_hostname")
db_database_api_key = os.getenv("db_database_api_keys")
db_database_ingest = os.getenv("db_database_ingest")
db_password = os.getenv("db_password")
db_table = os.getenv("db_table_api_key_users")
db_user = os.getenv("db_user")
db_port = os.getenv("db_port")

test_key = os.getenv("test_key")

def verify_api_key(api_key: str) -> str:

    try:

        conn = psycopg2.connect(
            host=db_hostname,
            database=db_database_api_key,
            user=db_user,
            password=db_password,
            port=db_port
        )

        # Create cursor
        cur = conn.cursor()

        # Execute query
        cur.execute(f"""SELECT id FROM {db_table}
                    WHERE api_key = '{api_key}'
                    AND database = '{db_database_ingest}'
                    AND write_access = 'Yes'""")

        # Fetch one result
        user_id = cur.fetchone()

        conn.close()

        if user_id == None:
            raise HTTPException(401)
        
        return user_id

    except psycopg2.Error:
        raise HTTPException(500)