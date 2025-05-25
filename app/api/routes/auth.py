from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, TokenResponse
from app.core.database import get_db
from app.core.security import get_password_hash, create_access_token
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Request
from app.core.security import verify_password,  create_refresh_token
from jose import JWTError, jwt
from app.core.config import settings
from app.models.client import Client
from pydantic import BaseModel, EmailStr
auth = APIRouter()
class LoginRequest(BaseModel):
    email: EmailStr
    password: str
@auth.post("/register", response_model=TokenResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    # Verificar se usuário ou email já existem
    existing_user = db.query(User).filter(
        (User.username == user.username) | (User.email == user.email)
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuário ou e-mail já cadastrado."
        )

   
    hashed_password = get_password_hash(user.password)

    # Criar novo usuário
    new_user = User(
        email=user.email,
        username=user.username,
        hashed_password=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    access_token = create_access_token(data={"sub": new_user.username})
    refresh_token = create_refresh_token(subject=new_user.username)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token, #
        "token_type": "bearer"
    }
@auth.post("/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    # Primeiro tenta buscar usuário admin (User)
    user = db.query(User).filter(User.email == request.email).first()
    if user and verify_password(request.password, user.hashed_password):
        role = "admin" if user.is_admin else "user"
        token = create_access_token(data={"sub": user.email, "role": role})
        return {"access_token": token, "token_type": "bearer"}

    # Se não achou usuário admin/user, tenta cliente normal
    client = db.query(Client).filter(Client.email == request.email).first()
    if client and verify_password(request.password, client.user.hashed_password):
        token = create_access_token(data={"sub": client.email, "role": "client"})
        return {"access_token": token, "token_type": "bearer"}

    # Se não encontrou nenhum, retorna erro
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Email ou senha incorretos.")
@auth.post("/refresh-token/", response_model=TokenResponse)
def refresh_token(request: Request):
    auth_header = request.headers.get("Authorization")

  
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token ausente ou invalido."
        )

    refresh_token = auth_header.split(" ")[1]

    try:
        payload = jwt.decode(
            refresh_token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )

        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Tipo de token inválido"
            )

        username = payload.get("sub")
        if not username:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido"
            )

      
        new_access_token = create_access_token(data={"sub": username, "type": "access"})
        new_refresh_token = create_refresh_token(subject=username)

        return {
            "access_token": new_access_token,
            "refresh_token": new_refresh_token,
            "token_type": "bearer"
        }

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token de refresh inválido ou expirado."
        )