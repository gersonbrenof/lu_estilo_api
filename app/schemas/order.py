from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from enum import Enum

class StatusPedido(str, Enum):
    PENDENTE = "pendente"
    PROCESSANDO = "processando"
    ENVIADO = "enviado"
    ENTREGUE = "entregue"
    CANCELADO = "cancelado"
class ItemPedidoCreate(BaseModel):
    produto_id: int
    quantidade: int
    preco_unitario_no_pedido: float

class PedidoCreate(BaseModel):
    cliente_id: int  # ou remova e pegue do current_user
    itens: List[ItemPedidoCreate]

class ItemPedidoOut(ItemPedidoCreate):
    id: int

    class Config:
        orm_mode = True

class PedidoUpdateStatus(BaseModel):
    status: StatusPedido

class PedidoOut(BaseModel):
    id: int
    cliente_id: int
    status: StatusPedido
    criado_em: datetime
    atualizado_em: datetime
    itens: List[ItemPedidoOut]

    class Config:
        orm_mode = True
class ItemPedidoCreate(BaseModel):
    produto_id: int
    quantidade: int
    preco_unitario_no_pedido: float

class PedidoCreateSemCliente(BaseModel):
    itens: List[ItemPedidoCreate]