from fastapi import Depends, HTTPException, status

from auth.dependencies import get_user
from database.schema import Users

def require_permission(admin: bool = False,
                       read: bool = False,
                       write: bool = False):

    async def permission_dependency(user: Users=Depends(get_user)):
        if admin and not user.is_admin:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="Admin permission required")
        
        if read and not user.can_read:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="Read permission required")
        
        if write and not user.can_write:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="Write permission required")
        
        return user
    
    return permission_dependency