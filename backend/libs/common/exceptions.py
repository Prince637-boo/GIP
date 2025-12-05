
from fastapi import HTTPException, status

def NotFoundException(detail="Resource not found"):
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)
