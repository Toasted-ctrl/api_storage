from app import auth
from app import models
from app.database import get_database, Ingest, Users, ApiKeys
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session

app = FastAPI(version="0.0.1", contact={"maintainer": "Toasted-ctrl"})
api_key_header = APIKeyHeader(name="api-key")
    
@app.get("/", response_model = models.ReturnRoot, tags=["Default"])
def get_root():
    
    return {"message": "Hello There",
            "version": app.version,
            "contact": app.contact}

@app.get("/health", response_model=models.ReturnHealth, tags=["Default"])
def get_health():
    
    return {"status": "OK"}

@app.post("/data/add_single", response_model=models.ReturnDataSingle, tags=["Data"])
def post_single(payload: models.InputDataSingle,
           db: Session = Depends(get_database),
           api_key: str = Depends(api_key_header)):
    
    user = auth.verify_api_key(database=db, api_key=auth.hash_key(api_key))
    auth.verify_resource_access(database=db, user_id=user.user_id, can_write=True)

    # TODO: Maybe this needs to be its own function, and added to app.database?

    # NOTE: This will dump everything in single db.
    # NOTE: ETL will be conducted at a later stage.
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

@app.get("/data/sources", response_model=models.ReturnDataSources, tags = ["Data"])
def get_data_sources(db: Session = Depends(get_database),
                     api_key = Depends(api_key_header)):
    
    user = auth.verify_api_key(database=db, api_key=auth.hash_key(api_key))
    auth.verify_resource_access(database=db, user_id=user.user_id, can_read=True)

    query = db.query(Ingest.url_primary, Ingest.url_extension).distinct().all()

    sources = {}
    for url_p, url_e in query:
        if url_p not in sources:
            sources[url_p] = []
            sources[url_p].append(url_e)
        else:
            sources[url_p].append(url_e)

    return {"message": "Success",
            "sources": sources}

@app.get("/users", response_model=models.ReturnUsers, tags=["Users"])
def get_users(db: Session = Depends(get_database),
              api_key = Depends(api_key_header)):
    
    user = auth.verify_api_key(database=db, api_key=auth.hash_key(api_key))
    auth.verify_resource_access(database=db, user_id=user.user_id, is_admin=True)

    query = db.query(Users.user_id, Users.email).distinct().all()

    users = {}
    for u_id, u_mail in query:
        users[u_id] = u_mail

    return {"message": "Success",
            "users": users}

@app.put("/users/retire/{user_id}", response_model=models.ReturnSimple, tags=["Users"])
def retire_user(user_id: int,
                db: Session = Depends(get_database),
                api_key = Depends(api_key_header)):
    
    user = auth.verify_api_key(database=db, api_key=auth.hash_key(key=api_key))
    auth.verify_resource_access(database=db, user_id=user.user_id, is_admin=True)

    user = db.query(Users).filter(Users.user_id == user_id).first()
    if user:
        # NOTE: If a user is located, we can just set the attribute is_active to False.
        user.is_active = False
        db.commit()
        return {"message": "Success"}
    else:
        raise HTTPException(status_code=404, detail="User does not exist")

@app.get("/users/{user_id}", response_model=models.ReturnUser, tags=["Users"])
def get_user(user_id: int,
             db: Session = Depends(get_database),
             api_key = Depends(api_key_header)):
    
    user = auth.verify_api_key(database=db, api_key=auth.hash_key(key=api_key))
    auth.verify_resource_access(database=db, user_id=user.user_id, is_admin=True)

    return {"message": "Success",
            "user": {
                "user_id": user_id}}

@app.post("/users/add_user", response_model=models.ReturnNewUser, tags=["Users"])
def post_user(payload: models.InputNewUser,
              db: Session = Depends(get_database),
              api_key: str = Depends(api_key_header)):
    
    user = auth.verify_api_key(database=db, api_key=auth.hash_key(api_key))
    auth.verify_resource_access(database=db, user_id=user.user_id, is_admin=True)

    new_user = Users(
        email = payload.email,
        first_name = payload.first_name,
        last_name = payload.last_name,
        is_admin = payload.is_admin,
        can_read = payload.can_read,
        can_write = payload.can_write,
        is_active = True)

    db.add(new_user)
    db.commit()

    # TODO: Implement error handling for if the new user cannot be located.
    # TODO: Implement rollback functionality

    # NOTE: .scalar() return the first column of the first result.
    # NOTE: Querying Users.user_id makes so we return only the user_id db column.
    new_user_id = db.query(Users.user_id).filter(Users.email == payload.email).scalar()

    if new_user_id == None:
        raise HTTPException(status_code=404, detail="Unexpected error: Unable to add new user")
    
    # NOTE: Returns a tuple, with [0] being the user key, and [1] being the hashed key.
    generated_keys = auth.generate_key(database=db)

    new_key = ApiKeys(
        hashed_api_key = generated_keys[1],
        user_id = new_user_id,
        is_valid = True
    )

    db.add(new_key)
    db.commit()
    
    return {"message": "Success",
            "new_user": {
                "email": payload.email,
                "api_key": generated_keys[0]}}