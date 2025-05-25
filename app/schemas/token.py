from pydantic import BaseModel
from typing import Optional

class Token(BaseModel):
    access_token: str
    token_type: str
    refresh_token: Optional[str] = None # Incluir refresh token na resposta de login

class TokenPayload(BaseModel):
    sub: Optional[str] = None
    role: Optional[str] = None # Para identificar o papel do usuário no token
    type: Optional[str] = None # 'access' ou 'refresh'

class TokenResponse(BaseModel): # O que é retornado no login/refresh
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class RefreshTokenRequest(BaseModel): # Se for passar o refresh token no body
    refresh_token: str