from pydantic import BaseModel

class ScanLogCreate(BaseModel):
    location: str
    device_info: str | None = None

class ScanLogOut(BaseModel):
    id: str
    location: str
    device_info: str | None
    timestamp: str

    class Config:
        from_attributes = True
