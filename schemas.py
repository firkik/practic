from pydantic import BaseModel, EmailStr
from typing import Optional

class DeviceScheme(BaseModel):
    name: str
    system: str
    memory: int
    components: bool = False
    

class UpdateDeviceScheme(BaseModel):
    name: Optional[str]
    system: Optional[str]
    memory: Optional[int]
    components: Optional[bool]
    
class UserCreate(BaseModel):
    email: str
    password: str
    
class UserOut(BaseModel):
    id: int
    email: EmailStr
    
class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
class TokenData(BaseModel):
    id: Optional[int] = None
    
class Token(BaseModel):
    access_token: str
    token_type: str