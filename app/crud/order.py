from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.order import Pedido, ItemPedido
from app.schemas.order import PedidoCreate, PedidoUpdateStatus, PedidoCreateSemCliente

def create_pedido(db: Session, cliente_id: int, pedido_in: PedidoCreateSemCliente):
    pedido = Pedido(cliente_id=cliente_id)
    db.add(pedido)
    db.flush()

    itens = [
        ItemPedido(
            pedido_id=pedido.id,
            produto_id=item.produto_id,
            quantidade=item.quantidade,
            preco_unitario_no_pedido=item.preco_unitario_no_pedido,
        )
        for item in pedido_in.itens
    ]

    db.add_all(itens)
    db.commit()
    db.refresh(pedido)
    return pedido

def get_pedido(db: Session, pedido_id: int) -> Optional[Pedido]:
    return db.query(Pedido).filter(Pedido.id == pedido_id).first()

def update_status_pedido(db: Session, pedido_id: int, status: str) -> Optional[Pedido]:
    pedido = get_pedido(db, pedido_id)
    if not pedido:
        return None
    pedido.status = status
    db.commit()
    db.refresh(pedido)
    return pedido

def list_pedidos(db: Session, skip: int = 0, limit: int = 100) -> List[Pedido]:
    return db.query(Pedido).offset(skip).limit(limit).all()
