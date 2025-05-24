from pydantic import BaseModel

class UserCreate(BaseModel):
    email: str
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    
