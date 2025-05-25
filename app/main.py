from fastapi import FastAPI
from app.api.routes.auth import auth
from app.api.routes.client import client
from app.core.database import Base, engine
from fastapi import Depends
from app.api.routes.product import product
from app.api.routes.order import order
from app.api.dependencies import get_current_user
app = FastAPI(title="LU Estilo API")


Base.metadata.create_all(bind=engine)
@app.get("/")
def read_root():
    return {"message": "Bem-vindo à API LU Estilo"}

# app.include_router(user_router, prefix="/users", tags=["users"])
app.include_router(auth, prefix="/auth",tags=['auth'] )
app.include_router(client, prefix="", tags=['clientes'])
app.include_router(product, prefix="", tags=["produtos"])
app.include_router(order, prefix="", tags=["pedidos"])