from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from app.models.client import Client
from app.core.database import get_db
from app.schemas.order import (
    PedidoCreate,
    PedidoOut,
    PedidoUpdateStatus,
)
from app.crud.order import (
    create_pedido,
    get_pedido,
    update_status_pedido,
)
from app.schemas.order import PedidoCreateSemCliente
from app.models.order import Pedido, ItemPedido, StatusPedido
from app.models.product import Product
from app.models.user import User
from app.api.dependencies import get_current_user

order = APIRouter()
@order.post("/orders", response_model=PedidoOut, status_code=status.HTTP_201_CREATED)
def criar_pedido(
    pedido_in: PedidoCreateSemCliente,  # pedido enviado pelo cliente, sem cliente_id
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> PedidoOut:
    # Cria o objeto PedidoCreate com cliente_id do usuário logado
    pedido_data = PedidoCreate.parse_obj({
    "cliente_id": current_user.id,
    "itens": [item.dict() for item in pedido_in.itens]
})
    # Chama a função real que cria no banco de dados
    pedido = create_pedido(db, pedido_data)

    return pedido

@order.get("/orders/{pedido_id}", response_model=PedidoOut)
def ler_pedido(
    pedido_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    pedido = get_pedido(db, pedido_id)
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")

    if pedido.cliente_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Não autorizado a ver este pedido")

    return pedido

@order.put("/orders/{pedido_id}/status", response_model=PedidoOut)
def atualizar_status_pedido(
    pedido_id: int,
    status_in: PedidoUpdateStatus,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    pedido = get_pedido(db, pedido_id)
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")

    if pedido.cliente_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Não autorizado a atualizar este pedido")

    pedido = update_status_pedido(db, pedido_id, status_in)
    return pedido

@order.get("/orders", response_model=List[PedidoOut])
def listar_pedidos(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=100),
    data_inicio: Optional[datetime] = Query(None),
    data_fim: Optional[datetime] = Query(None),
    secao: Optional[str] = Query(None),
    pedido_id: Optional[int] = Query(None),
    status: Optional[StatusPedido] = Query(None),
    cliente_id: Optional[int] = Query(None),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Pedido)

    if pedido_id is not None:
        query = query.filter(Pedido.id == pedido_id)

    if status is not None:
        query = query.filter(Pedido.status == status)

    if cliente_id is not None:
        query = query.filter(Pedido.cliente_id == cliente_id)

    if data_inicio is not None:
        query = query.filter(Pedido.criado_em >= data_inicio)
    if data_fim is not None:
        query = query.filter(Pedido.criado_em <= data_fim)

    if secao is not None:
        query = query.join(Pedido.itens).join(ItemPedido.produto).filter(Product.secao.ilike(f"%{secao}%"))

    if not current_user.is_admin:
        # Buscar client relacionado ao usuário logado
        client = db.query(Client).filter(Client.user_id == current_user.id).first()
        if not client:
            raise HTTPException(status_code=404, detail="Cliente não encontrado para o usuário logado")
        query = query.filter(Pedido.cliente_id == client.id)

    pedidos = query.offset(skip).limit(limit).all()
    return pedidos
