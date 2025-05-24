from sqlalchemy.orm import Session
from app.models.client import Client
from app.schemas.client import ClientCreate

def get_client_by_email(db: Session, email: str):
    return db.query(Client).filter(Client.email == email).first()

def get_client_by_cpf(db: Session, cpf: str):
    return db.query(Client).filter(Client.cpf == cpf).first()

def create_client(db: Session, client: ClientCreate):
    # Valida email e cpf únicos
    if get_client_by_email(db, client.email):
        raise ValueError("Email já cadastrado")
    if get_client_by_cpf(db, client.cpf):
        raise ValueError("CPF já cadastrado")

    db_client = Client(nome=client.nome, email=client.email, cpf=client.cpf)
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client