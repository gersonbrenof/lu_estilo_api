from pydantic import BaseModel, EmailStr, constr
from typing import Optional
class ClientCreate(BaseModel):
    nome: str
    email: EmailStr
    cpf: constr(min_length=11, max_length=14)
    

class ClientResponse(BaseModel):
    id: int
    nome: str  
    email: EmailStr
    cpf: str

    class Config:
        orm_mode = True
        
class ClientUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[EmailStr] = None
    cpf: Optional[constr(min_length=11, max_length=14)] = None