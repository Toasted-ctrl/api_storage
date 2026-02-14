import os
import psycopg2

from dotenv import load_dotenv
from fastapi import HTTPException

load_dotenv()

db_hostname = os.getenv("db_hostname")
db_database = os.getenv("db_database_api_keys")
db_password = os.getenv("db_password")
db_table = os.getenv("db_table_api_key_users")
db_user = os.getenv("db_user")
db_port = os.getenv("db_port")

def verify_api_key(api_key: str, database: str, access_type: str) -> str:

    try:

        conn = psycopg2.connect(
            host=db_hostname,
            database=db_database,
            user=db_user,
            password=db_password,
            port=db_port
        )

        # Create cursor
        cur = conn.cursor()

        # Execute query
        cur.execute(f"""SELECT id FROM {db_table}
                    WHERE api_key = '{api_key}'
                    AND database = '{database}'
                    AND access_type = '{access_type}'""")

        # Fetch one result
        user_id = cur.fetchone()

        if user_id == None:
            raise HTTPException(status_code=401)
        
        return user_id
    
    except HTTPException as httpe:
        raise HTTPException(status_code=httpe.status_code, detail=httpe.detail)

    except psycopg2.Error:
        raise HTTPException(500)
    
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()