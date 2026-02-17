import os
import psycopg2

from datetime import datetime
from dotenv import load_dotenv
from fastapi import HTTPException, Security
from fastapi.security import APIKeyHeader
from typing import Callable

load_dotenv()

db_hostname = os.getenv("db_hostname")
db_database = os.getenv("db_database_api_keys")
db_password = os.getenv("db_password")
db_table = os.getenv("db_table_api_key_users")
db_user = os.getenv("db_user")
db_port = os.getenv("db_port")

api_key_header = APIKeyHeader(name="API_KEY")

# TODO: Build function to test this feature.
def verify_api_key(is_admin: bool = False) -> Callable[[str], dict[int, str]]:

    def api_key_dependencies(api_key: str = Security(api_key_header)) -> dict[int, str]:

        try:

            conn = psycopg2.connect(
                database=db_database,
                user=db_user,
                password=db_password,
                host=db_hostname,
                port=db_port
            )

            cursor = conn.cursor()

            current_time = datetime.now()

            query = f"SELECT id FROM {db_table} WHERE api_key = '{api_key}' AND expiry_date > '{current_time}'"

            if is_admin == True:
                query = f"SELECT id FROM {db_table} WHERE api_key = '{api_key}' AND expiry_date > '{current_time}' AND is_admin = 'True'"

            cursor.execute(query=query)

            user_id = cursor.fetchone()

            if user_id == None:
                raise HTTPException(403)
            
            if cursor is not None: # TODO: Investigate if this is the proper way to handle.
                cursor.close()

            if conn is not None: # TODO: Investigate if this is the proper way to handle.
                conn.close()
        
            return {"user_id": user_id, "api_key": api_key}
        
        except HTTPException as httpe:
            raise HTTPException(httpe.status_code, detail=httpe.detail)
        
        except psycopg2.Error:
            raise HTTPException(500, detail="Unknown Server Error: DB query")
        
        except Exception:
            raise HTTPException(500, detail='Unknown Server Error')
    
    return api_key_dependencies