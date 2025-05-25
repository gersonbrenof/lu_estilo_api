# from fastapi import APIRouter, Depends, Query, HTTPException, status
# from sqlalchemy.orm import Session
# from typing import List, Optional
# from app.schemas.order import PedidoCreate, PedidoOut, PedidoUpdate
# from app.crud import order as crud_order
# from app.core.database import get_db
# from app.api.dependencies import get_current_user
# from app.models.client import Client  # modelo de usuário autenticado
# from app.models.user import User

# order = APIRouter()

# @order.get("/orders", response_model=List[PedidoOut])
# def listar_pedidos(
#     status: Optional[str] = Query(None),
#     client_id: Optional[int] = Query(None),
#     id: Optional[int] = Query(None),
#     db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_user),
# ):
#     filtros = {k: v for k, v in {"status": status, "client_id": client_id, "id": id}.items() if v is not None}
#     return crud_order.get_pedidos(db, filtros)

# @order.post("/orders", response_model=PedidoOut, status_code=201)
# def criar_pedido(
#     pedido: PedidoCreate,
#     db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_user),
# ):
#     return crud_order.create_pedido(db, pedido)

# @order.get("/orders/{pedido_id}", response_model=PedidoOut)
# def obter_pedido(
#     pedido_id: int,
#     db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_user),
# ):
#     pedido = crud_order.get_pedido(db, pedido_id)
#     if not pedido:
#         raise HTTPException(status_code=404, detail="Pedido não encontrado")
#     return pedido

# @order.put("/orders/{pedido_id}", response_model=PedidoOut)
# def atualizar_pedido(
#     pedido_id: int,
#     pedido: PedidoUpdate,
#     db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_user),
# ):
#     return crud_order.update_pedido(db, pedido_id, pedido)

# @order.delete("/orders/{pedido_id}", status_code=204)
# def excluir_pedido(
#     pedido_id: int,
#     db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_user),
# ):
#     crud_order.delete_pedido(db, pedido_id)
