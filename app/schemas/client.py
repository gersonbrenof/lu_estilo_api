from pydantic import BaseModel, EmailStr, constr
from typing import Optional

class ClientBase(BaseModel):
    nome: str
    email: EmailStr
    cpf: constr(min_length=11, max_length=14)

class ClientCreate(ClientBase):
    senha: str  # senha para criar o User também

class ClientUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[EmailStr] = None
    cpf: Optional[constr(min_length=11, max_length=14)] = None
    senha: Optional[str] = None

class ClientResponse(ClientBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True
class ClientWithTokenResponse(BaseModel):
    client: ClientResponse
    token: str