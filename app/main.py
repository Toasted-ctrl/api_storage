from app import auth
from app import models
from app.database import get_database, Ingest, Users, ApiKeys
from fastapi import FastAPI, Depends, HTTPException
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

    # NOTE: This will dump everything in single db.
    # NOTE: ETL will be conducted at a later statge.
    new_ingest_item = Ingest(
        url_primary = payload.url_primary,
        url_extension = payload.url_extension,
        params = payload.params,
        status_code = payload.status_code,
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
        email = payload.email,
        first_name = payload.first_name,
        last_name = payload.last_name,
        is_admin = payload.is_admin,
        can_read = payload.can_read,
        can_write = payload.can_write)

    db.add(new_user)
    db.commit()

    # TODO: Implement error handling for if the new user cannot be located.
    # TODO: Implement rollback functionality
    # TODO: Implement hashing so we don't store the raw key.

    # NOTE: .scalar() return the first column of the first result.
    # NOTE: Querying Users.user_id makes so we return only the user_id db column.
    new_user_id = db.query(Users.user_id).filter(Users.email == payload.email).scalar()

    if new_user_id == None:
        raise HTTPException(404, detail="Unexpected error: Unable to add new user")
    
    generated_key = auth.generate_key(database=db)

    new_key = ApiKeys(
        api_key = generated_key,
        user_id = new_user_id
    )

    db.add(new_key)
    db.commit()
    
    return {"message": "Success",
            "new_user": {
                "email": payload.email,
                "api_key": generated_key,
                "expiry_date": payload.expiry_date}}