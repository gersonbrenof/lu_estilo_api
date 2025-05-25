from fastapi import APIRouter, Depends, HTTPException, status, Query, Path
from sqlalchemy.orm import Session
from typing import List, Optional

from app.schemas.client import ClientCreate, ClientResponse, ClientUpdate, ClientWithTokenResponse
from app.crud.client import create_client
from app.core.database import get_db
from app.api.dependencies import get_current_user, check_user_role
from app.models.client import Client
from app.core.security import create_access_token
from sqlalchemy.exc import IntegrityError
from app.models.user import User
client = APIRouter()


@client.post("/clients", response_model=ClientWithTokenResponse, status_code=status.HTTP_201_CREATED)
def create_new_client(
    client_in: ClientCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    check_user_role(current_user)  # só usuário autorizado pode criar

    try:
        # Verifica se já existe usuário com o mesmo email/username
        existing_user = db.query(User).filter(User.username == client_in.email).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Usuário com este email já existe")

        client_db = create_client(db, client_in)

    except IntegrityError:
        # Captura erro do banco e lança HTTPException amigável
        raise HTTPException(status_code=400, detail="Erro: usuário já cadastrado")
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    token = create_access_token({"sub": client_db.email})

    return ClientWithTokenResponse(client=client_db, token=token)

@client.get("/clients", response_model=List[ClientResponse])
def list_clients(
    skip: int = 0,
    limit: int = 10,
    nome: Optional[str] = Query(None, description="Filtra clientes pelo nome (parcial)"),
    email: Optional[str] = Query(None, description="Filtra clientes pelo email (parcial)"),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    # Qualquer usuário autenticado pode listar clientes
    check_user_role(current_user)  
    query = db.query(Client)

    if nome:
        query = query.filter(Client.nome.ilike(f"%{nome}%"))
    if email:
        query = query.filter(Client.email.ilike(f"%{email}%"))

    clients = query.offset(skip).limit(limit).all()
    return clients


@client.get("/clients/{id}", response_model=ClientResponse)
def get_client_by_id(
    id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    check_user_role(current_user)  
    client_db = db.query(Client).filter(Client.id == id).first()
    if not client_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente não encontrado")
    return client_db


@client.put("/clients/{id}", response_model=ClientResponse)
def update_client(
    client_in: ClientUpdate,
    id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    check_user_role(current_user)  # só usuário autorizado pode atualizar

    client_db = db.query(Client).filter(Client.id == id).first()
    if not client_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente não encontrado")

    # Verificar unicidade de email, se email foi passado para atualizar
    if client_in.email and client_in.email != client_db.email:
        email_exists = db.query(Client).filter(Client.email == client_in.email, Client.id != id).first()
        if email_exists:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email já cadastrado para outro cliente.")

    # Verificar unicidade de cpf, se cpf foi passado para atualizar
    if client_in.cpf and client_in.cpf != client_db.cpf:
        cpf_exists = db.query(Client).filter(Client.cpf == client_in.cpf, Client.id != id).first()
        if cpf_exists:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="CPF já cadastrado para outro cliente.")

    # Atualizar somente os campos que foram enviados
    if client_in.nome is not None:
        client_db.nome = client_in.nome
    if client_in.email is not None:
        client_db.email = client_in.email
    if client_in.cpf is not None:
        client_db.cpf = client_in.cpf

    db.commit()
    db.refresh(client_db)

    return client_db


@client.delete("/clients/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_client(
    id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    check_user_role(current_user)  # só usuário autorizado pode deletar
    
    client_db = db.query(Client).filter(Client.id == id).first()
    if not client_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente não encontrado")
    
    db.delete(client_db)
    db.commit()
    return
