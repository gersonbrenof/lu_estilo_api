from sqlalchemy.orm import Session
from app.models.client import Client
from app.models.user import User
from app.core.security import get_password_hash  # sua função para hash da senha
from app.schemas.client import ClientCreate,ClientUpdate
def get_client(db: Session, client_id: int):
    return db.query(Client).filter(Client.id == client_id).first()

def get_client_by_email(db: Session, email: str):
    return db.query(Client).filter(Client.email == email).first()

def create_client(db: Session, client_data: ClientCreate):
    # Criar o User primeiro
    user = User(
        email=client_data.email,
        username=client_data.email,  # ou outro critério para username
        hashed_password=get_password_hash(client_data.senha),
        is_admin=False
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    # Criar Client vinculado ao User
    client = Client(
        nome=client_data.nome,
        email=client_data.email,
        cpf=client_data.cpf,
        user_id=user.id
    )
    db.add(client)
    db.commit()
    db.refresh(client)
    return client

def update_client(db: Session, client: Client, updates: ClientUpdate):
    if updates.nome is not None:
        client.nome = updates.nome
    if updates.email is not None:
        client.email = updates.email
    if updates.cpf is not None:
        client.cpf = updates.cpf
    if updates.senha is not None:
        # Atualiza a senha do usuário associado
        client.user.hashed_password = get_password_hash(updates.senha)
        db.add(client.user)
    db.add(client)
    db.commit()
    db.refresh(client)
    return client

def delete_client(db: Session, client: Client):
    # Deleta client e o user associado
    db.delete(client)
    if client.user:
        db.delete(client.user)
    db.commit()
