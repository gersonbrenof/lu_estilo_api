import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.database import SessionLocal
from sqlalchemy.orm import Session
from app.models.user import User
from app.core.security import get_password_hash
from app.core.database import Base, engine
@pytest.fixture()
def client():
    with TestClient(app) as c:
        yield c

@pytest.fixture()
def db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.rollback()
        db.close()

def test_register_user_success(client):
    response = client.post("/auth/register", json={
        "username": "unique_user_1",
        "email": "unique1@example.com",
        "password": "123456"
    })
    assert response.status_code == 200
    assert "refresh_token" in response.json()

def test_register_user_duplicate_email(client, db_session):
    # Criar usuário duplicado diretamente no DB para garantir que existe
    user = User(
        username="existinguser",
        email="existing@example.com",
        hashed_password=get_password_hash("password")
    )
    db_session.add(user)
    db_session.commit()

    payload = {
        "username": "newuser",
        "email": "existing@example.com",  # email duplicado
        "password": "newpassword"
    }

    response = client.post("/auth/register", json=payload)
    assert response.status_code == 400
    assert "Usuário ou e-mail já cadastrado." in response.json().get("detail", "")

def test_login_user_success(client):
    # Primeiro registra o usuário
    client.post("/register", json={
        "username": "login_user",
        "email": "login@example.com",
        "password": "123456"
    })

    # Depois tenta logar
    response = client.post("/auth/login", json={
        "email": "login@example.com",
        "password": "123456"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_user_wrong_password(db_session, client):
    email = "wrongpass@example.com"
    password = "correctpassword"
    hashed_password = get_password_hash(password)
    user = User(username="wrongpassuser", email=email, hashed_password=hashed_password)
    db_session.add(user)
    db_session.commit()

    payload = {
        "email": email,
        "password": "wrongpassword"
    }

    response = client.post("/auth/login", json=payload)
    assert response.status_code == 401
    assert response.json()["detail"] == "Email ou senha incorretos."
@pytest.fixture(scope="function", autouse=True)
def setup_and_teardown_db():
    # Cria as tabelas antes do teste
    Base.metadata.create_all(bind=engine)
    yield
    # Limpa todas as tabelas depois do teste
    Base.metadata.drop_all(bind=engine)