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

@app.post("/data", response_model=models.ReturnAddData, tags=["Data"])
def post_data(payload: models.InputAddData,
                db: Session = Depends(get_database),
                api_key: str = Depends(api_key_header)):
    
    v_key = auth.verify_api_key(database=db, api_key=auth.hash_key(api_key))
    auth.verify_resource_access(database=db, user_id=v_key.user_id, can_write=True)

    # NOTE: ETL will be conducted at a later stage.
    db.add_all([Ingest(**entry.model_dump()) for entry in payload.entries])
    db.commit()
    
    return {"message": "Success",
            "entries": payload.entries}

@app.get("/data/sources", response_model=models.ReturnDataSources, tags = ["Data"])
def get_data_sources(db: Session = Depends(get_database),
                     api_key = Depends(api_key_header)):
    
    v_key = auth.verify_api_key(database=db, api_key=auth.hash_key(api_key))
    auth.verify_resource_access(database=db, user_id=v_key.user_id, can_read=True)

    sources = db.query(Ingest.url_primary, Ingest.url_extension).distinct().all()
    if not sources:
        raise HTTPException(status_code=404, detail="Ingest database empty")

    return {"message": "Success",
            "sources": sources}

@app.get("/users", response_model=models.ReturnUsers, tags=["Users"])
def get_users(db: Session = Depends(get_database),
              api_key = Depends(api_key_header)):
    
    v_key = auth.verify_api_key(database=db, api_key=auth.hash_key(api_key))
    auth.verify_resource_access(database=db, user_id=v_key.user_id, is_admin=True)

    users = db.query(Users.user_id, Users.email).distinct().all()

    return {"message": "Success",
            "users": users}

@app.post("/users", response_model=models.ReturnNewUser, tags=["Users"])
def post_user(payload: models.InputNewUser,
              db: Session = Depends(get_database),
              api_key: str = Depends(api_key_header)):
    
    v_key = auth.verify_api_key(database=db, api_key=auth.hash_key(api_key))
    auth.verify_resource_access(database=db, user_id=v_key.user_id, is_admin=True)

    user_data = Users(**payload.model_dump())
    user_data.is_active = True

    db.add(user_data)
    db.commit()

    user = db.query(Users).filter(Users.email == payload.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="Unexpected error: Unable to add new user")
    
    # NOTE: Returns a tuple, with [0] being the user key, and [1] being the hashed key.
    n_keys = auth.generate_key(database=db)

    user_key = ApiKeys(
        hashed_api_key = n_keys[1],
        user_id = user.user_id,
        is_valid = True
    )

    db.add(user_key)
    db.commit()
    
    return {"message": "Success",
            "new_user": {
                "user": user,
                "api_key": n_keys[0]}}

@app.put("/users/{user_id}", response_model=models.ReturnUpdatedUser, tags=["Users"])
def update_user(user_id: int,
                payload: models.InputUpdateUser,
                db: Session = Depends(get_database),
                api_key: str = Depends(api_key_header)):
    
    v_key = auth.verify_api_key(database=db, api_key=auth.hash_key(key=api_key))
    auth.verify_resource_access(database=db, user_id=v_key.user_id, is_admin=True)

    user = db.query(Users).filter(Users.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    updates = payload.model_dump(exclude_none=True)
    if not updates:
        raise HTTPException(status_code=400, detail="No updates provided")
    
    for item, value in updates.items():
        setattr(user, item, value)

    db.commit()
    
    return {"message": "Success",
            "updates": len(updates),
            "user": user}

@app.get("/users/{user_id}", response_model=models.ReturnUser, tags=["Users"])
def get_user(user_id: int,
             db: Session = Depends(get_database),
             api_key = Depends(api_key_header)):
    
    v_key = auth.verify_api_key(database=db, api_key=auth.hash_key(key=api_key))
    auth.verify_resource_access(database=db, user_id=v_key.user_id, is_admin=True)

    user = db.query(Users).filter(Users.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {"message": "Success",
            "user": user}