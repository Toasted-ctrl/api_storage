import os

from dotenv import load_dotenv
from fastapi import HTTPException

load_dotenv()

test_key = os.getenv("test_key")

def is_allowed_post(api_key: str, access_type: str):
    if api_key != test_key: #TODO: Build function to verify api key
        raise HTTPException(401)