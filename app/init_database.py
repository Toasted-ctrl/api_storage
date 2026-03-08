import os

from database import base, engine, ApiKeys, Users
from dotenv import load_dotenv
from sqlalchemy.orm import Session

def init_db(engine: Session):
    print(">> Starting table creation")
    base.metadata.create_all(bind=engine)
    print(">> Tables created")

init_db(engine=engine)

load_dotenv()
key = os.getenv("ApiKey_key_hashed")
user_first_name = os.getenv("User_first_name")
user_last_name = os.getenv("User_last_name")
user_email = os.getenv("User_email")

def add_admin():

    print(">> Starting Admin User creation")

    db = Session(engine)

    try:

        admin_key = ApiKeys(
            hashed_api_key = key,
            user_id = 1,
            is_valid = True
        )

        db.add(admin_key)
        db.commit()
        print(">> Inserted: Admin Key")

        admin_user = Users(
            user_id = 1,
            email = user_email,
            first_name = user_first_name,
            last_name = user_last_name,
            is_active = True,
            is_admin = True,
            can_read = True,
            can_write = True
        )

        db.add(admin_user)
        db.commit()
        print(">> Inserted: Admin User")
        print(">> Admin User created ")

    except Exception:
        print(">> Unexpected error occured while creating admin user")

    finally:
        db.close()

add_admin()