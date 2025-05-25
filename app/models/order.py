import enum
from typing import List, TYPE_CHECKING
from datetime import datetime
from sqlalchemy import Integer, String, Float, Date, Boolean, ForeignKey, DateTime, ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from sqlalchemy.types import Enum as SAEnum
from app.core.database import Base

if TYPE_CHECKING:
    from .client import Client
    from .product import Product

class StatusPedido(str, enum.Enum):
    PENDENTE = "pendente"
    PROCESSANDO = "processando"
    ENVIADO = "enviado"
    ENTREGUE = "entregue"
    CANCELADO = "cancelado"

class Pedido(Base):
    __tablename__ = "pedidos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    cliente_id: Mapped[int] = mapped_column(ForeignKey("clients.id"), nullable=False)
    status: Mapped[StatusPedido] = mapped_column(
        SAEnum(StatusPedido, name="statuspedido_enum"),
        default=StatusPedido.PENDENTE,
        nullable=False
    )
    criado_em: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    atualizado_em: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    cliente: Mapped["Client"] = relationship("Client", back_populates="pedidos")
    itens: Mapped[List["ItemPedido"]] = relationship("ItemPedido", back_populates="pedido", cascade="all, delete-orphan")

class ItemPedido(Base):
    __tablename__ = "itens_pedido"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    pedido_id: Mapped[int] = mapped_column(ForeignKey("pedidos.id"), nullable=False)
    produto_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False)
    quantidade: Mapped[int] = mapped_column(Integer, nullable=False)
    preco_unitario_no_pedido: Mapped[float] = mapped_column(Float, nullable=False)

    pedido: Mapped["Pedido"] = relationship("Pedido", back_populates="itens")
    produto: Mapped["Product"] = relationship("Product")