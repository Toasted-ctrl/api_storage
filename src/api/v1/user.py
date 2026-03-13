from fastapi import APIRouter, Depends, HTTPException

from src.auth.permissions import require_permission
from src.database.session import get_db
from src.models.user import PayloadNewUser, ReturnNewUser, ReturnUsers
from src.services.user_service import UserService

# NOTE: Adding dependency in the route since we don't need the user object after
# NOTE: We can do this at the router already as checking users are admin-only features
router = APIRouter(dependencies=[Depends(require_permission(admin=True))])
tags = ["Users"]

def get_user_service(session=Depends(get_db)) -> UserService:
    return UserService(session=session)

@router.get("/users", tags=tags, response_model=ReturnUsers)
def get_users(user_service: UserService = Depends(get_user_service)):
    users = user_service.get_users()
    if not users:
        raise HTTPException(status_code=404, detail="No users in 'users' table")
    return {
        "detail": "Success",
        "users": users
    }

@router.post("/users", tags=tags, response_model=ReturnNewUser)
def post_user(payload: PayloadNewUser, user_service: UserService = Depends(get_user_service)):
    user = user_service.post_user(data=payload.model_dump())
    if not user:
        raise HTTPException(status_code=500, detail="Unable to add user")
    
    # TODO: Implement key generation.
    return {
        "detail": "Success",
        "new_user": {
            "user": user,
            "api_key": "test_key"
        }
    }

# TODO: Add function to update user.