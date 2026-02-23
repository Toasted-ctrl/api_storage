from app import auth
from app import models
from app.database import get_database, Ingest, Users
from fastapi import FastAPI, Depends
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session

app = FastAPI(version="0.0.1", contact={"maintainer": "Toasted-ctrl"})
api_key_header = APIKeyHeader(name="api-key")
    
@app.get("/", response_model = models.ReturnRoot)
def root():
    
    return {"message": "Hello There",
            "version": app.version,
            "contact": app.contact}

@app.get("/health", response_model=models.ReturnHealth)
def health():
    
    return {"status": "OK"}

@app.post("/single", response_model = models.ReturnDataSingle)
def single(payload: models.InputDataSingle,
           db: Session = Depends(get_database),
           api_key: str = Depends(api_key_header)):
    
    user = auth.verify_api_key(database=db, api_key=api_key)
    auth.verify_resource_access(database=db, user_id=user.user_id, can_write=True)

    # TODO: Maybe this needs to be its own function, and added to app.database?
    new_ingest_item = Ingest(
        url_primary = payload.url_primary,
        url_extension = payload.url_extension,
        params = payload.params,
        data = payload.data)
    
    db.add(new_ingest_item)
    db.commit()
    
    return {"message": "Success",
            "url_primary": payload.url_primary,
            "url_extension": payload.url_extension,
            "params": payload.params,
            "data": payload.data}

@app.post("/add_user", response_model = models.ReturnNewUser)
def add_user(payload: models.InputNewUser,
             db: Session = Depends(get_database),
             api_key: str = Depends(api_key_header)):
    
    user = auth.verify_api_key(database=db, api_key=api_key)
    auth.verify_resource_access(database=db, user_id=user.user_id, is_admin=True)

    new_user = Users(
        first_name = payload.first_name,
        last_name = payload.last_name,
        is_admin = payload.is_admin,
        can_read = payload.can_read,
        can_write = payload.can_write)

    db.add(new_user)
    db.commit()

    # TODO: Implement new functionality so that only unique combinations of first and last name may be added.
    # TODO: Implement error handling for if the new user cannot be located.
    # TODO: Implement functionality to create a new unique api key, and add this key to ApiKey.
    # TODO: Should we start this as a transaction, and if something fails, do a rollback?
    # TODO: Should probably have its own function under app.database.
    added_user = db.query(Users).filter(Users.first_name == payload.first_name, Users.last_name == payload.last_name).first()

    # TODO: Finalize implementation
    
    return {"message": "Success",
            "api_key": api_key,
            "new_user_api_key": "TEST-KEY-NEW-USER-123",
            "expiry_date": payload.expiry_date}