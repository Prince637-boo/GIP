from fastapi import Depends, HTTPException, status
from services.auth.dependencies.user import get_current_user
from services.auth.core.roles import UserRole

def allow(*roles: UserRole):
    async def wrapper(current_user = Depends(get_current_user)):
        if current_user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
        return current_user
    return wrapper
