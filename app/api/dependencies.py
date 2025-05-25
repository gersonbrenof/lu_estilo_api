from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from app.models.user import User # Ajuste o caminho se necessário
from app.core.database import get_db # Ajuste o caminho se necessário
from app.core.config import settings # <--- IMPORTAR settings
from sqlalchemy.orm import Session
# Remova essas linhas se elas estiverem aqui:
# import os
# SECRET_KEY = os.getenv("SECRET_KEY", "segredo")
# ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login") # ou "/auth/login/" dependendo da sua rota

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )
        user_email: str = payload.get("sub")
        if user_email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.email == user_email).first()
    if user is None:
        raise credentials_exception
    return user
def check_user_role(current_user: User, required_admin: bool = True):
    """
    Verifica se o usuário tem permissão de administrador.
    Se required_admin for True, o usuário precisa ser admin para passar.
    """
    if required_admin and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Acesso negado: privilégios insuficientes")