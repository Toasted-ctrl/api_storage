from fastapi import APIRouter, Depends, HTTPException, status

from auth.permissions import require_permission
from database.session import get_db
from models.user import PayloadNewUser, ReturnNewUser, ReturnUsers, ReturnUser
from services.user_service import UserService

# NOTE: Adding dependency in the route since we don't need the user object after
# NOTE: We can do this at the router already as checking users are admin-only features
router = APIRouter(dependencies=[Depends(require_permission(admin=True))])
tags = ["Users"]

def get_user_service(session=Depends(get_db)) -> UserService:
    return UserService(session=session)

@router.get("/users", tags=tags, response_model=ReturnUsers)
def get_users(user_service: UserService=Depends(get_user_service)):
    users = user_service.get_users()
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No users in 'users' table")
    return {
        "detail": "Success",
        "users": users
    }

@router.post("/users", tags=tags, response_model=ReturnNewUser)
def post_user(payload: PayloadNewUser, user_service: UserService=Depends(get_user_service)):
    new_user = user_service.post_user(data=payload.model_dump())
    if not new_user:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unable to add user")
    return {
        "detail": "Success",
        "new_user": {
            "user": new_user[0],
            "api_key": new_user[1]
        }
    }

# TODO: Implement tests for the below function.
@router.get("/users/{user_id}", tags=tags, response_model=ReturnUser)
def get_user(user_id: int, user_service: UserService=Depends(get_user_service)):
    user = user_service.get_user(id=user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return {
        "detail": "Success",
        "user": user
    }

# TODO: Add function to update user.