import os
import sys

from dotenv import load_dotenv
from sqlalchemy.orm import Session

from auth.hashing import hash_sha256
from database.schema import Base, Users, ApiKeys
from database.session import engine, get_db

if __name__ == '__main__':

    print("\n--- Starting Table Creation ---\n")

    try:
        Base.metadata.create_all(bind=engine)
        print(">> Added 'ingest', 'api_keys' and 'users' table to the database.")
    except Exception:
        print("UNEXPECTED ERROR: Please check that the database instance is running.")
        sys.exit()

    load_dotenv()
    if os.getenv("include_admin_user") == "true":

        print("\n--- Creating System User ---\n")

        try:
            print(">> Loading user data")

            first_name = os.getenv("system_user_first_name")
            last_name = os.getenv("system_user_last_name")
            unhashed_key = os.getenv("system_user_unhashed_key")
            email = os.getenv("system_user_email")

            print(">> Creating hashed key")
            hashed_key = hash_sha256(input=unhashed_key)

            print(">> Initiating database connection")
            db: Session = next(get_db())

            print(">> Inserting System User to user table")
            user = Users(
                email=email,
                first_name=first_name,
                last_name=last_name,
                is_admin=True,
                can_read=True,
                can_write=True,
                is_active=True
            )

            db.add(user)
            db.commit()

            print(">> Fetching user_id")
            user_id = db.query(Users.user_id).filter(Users.email == email).scalar()

            print(">> Inserting System User API key")
            key = ApiKeys(
                hashed_api_key=hashed_key,
                is_valid=True,
                user_id=user_id
            )

            db.add(key)
            db.commit()

        except Exception:
            print("UNEXPECTED ERROR: Unable to create System User")

    print("\n--- DATABASE INITIALIZATION COMPLETE ---\n")