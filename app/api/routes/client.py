from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.schemas.client import ClientCreate, ClientResponse, ClientUpdate
from app.crud.client import create_client
from app.core.database import get_db
from app.api.dependencies import get_current_user 
from typing import List, Optional
from app.models.client import Client
from fastapi import Path
client = APIRouter()

@client.post("/clients", response_model=ClientResponse, status_code=201)
def create_new_client(
    client_in: ClientCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user), 
):
    try:
        client = create_client(db, client_in)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return client

@client.get("/clients", response_model=List[ClientResponse])
def list_clients(
    skip: int = 0,
    limit: int = 10,
    nome: Optional[str] = Query(None),
    email: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    query = db.query(Client)

    if nome:
        query = query.filter(Client.nome.ilike(f"%{nome}%"))
    if email:
        query = query.filter(Client.email.ilike(f"%{email}%"))

    clients = query.offset(skip).limit(limit).all()
    return clients


@client.delete("/clients/{id}", status_code=204)
def delete_client(
    id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    client_db = db.query(Client).filter(Client.id == id).first()
    if not client_db:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    
    db.delete(client_db)
    db.commit()
    return

@client.get("/clients/{id}", response_model=ClientResponse)
def get_client_by_id(
    id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    client_db = db.query(Client).filter(Client.id == id).first()
    if not client_db:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return client_db


@client.put("/clients/{id}", response_model=ClientResponse)
def update_client(
    client_in: ClientUpdate,
    id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    client_db = db.query(Client).filter(Client.id == id).first()
    if not client_db:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    
    # Verificar se email ou cpf já existem em outro cliente (únicos)
    email_exists = db.query(Client).filter(Client.email == client_in.email, Client.id != id).first()
    if email_exists:
        raise HTTPException(status_code=400, detail="Email já cadastrado para outro cliente.")
    
    cpf_exists = db.query(Client).filter(Client.cpf == client_in.cpf, Client.id != id).first()
    if cpf_exists:
        raise HTTPException(status_code=400, detail="CPF já cadastrado para outro cliente.")
    

    client_db.nome = client_in.nome
    client_db.email = client_in.email
    client_db.cpf = client_in.cpf

    db.commit()
    db.refresh(client_db)

    return client_db