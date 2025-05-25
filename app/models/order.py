# import enum
# from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum as SAEnum, DateTime
# from sqlalchemy.orm import Mapped, mapped_column, relationship
# from sqlalchemy.sql import func # Para default timestamp
# from typing import List, TYPE_CHECKING
# from app.core.database import Base
# from datetime import datetime # <--- ADICIONE ESTA LINHA

# if TYPE_CHECKING:
#     from .client import Client
#     from .product import Product

# class OrderStatus(str, enum.Enum):
#     PENDENTE = "pendente"
#     PROCESSANDO = "processando"
#     ENVIADO = "enviado"
#     ENTREGUE = "entregue"
#     CANCELADO = "cancelado"

# class Order(Base):
#     __tablename__ = "orders"

#     id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
#     client_id: Mapped[int] = mapped_column(ForeignKey("clients.id"), nullable=False)
#     status: Mapped[OrderStatus] = mapped_column(SAEnum(OrderStatus), default=OrderStatus.PENDENTE, nullable=False)
#     # Usando o datetime importado aqui
#     created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
#     updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
#     # total_amount: Mapped[float] = mapped_column(Float, nullable=False) # Pode ser calculado

#     client: Mapped["Client"] = relationship(back_populates="orders")
#     items: Mapped[List["OrderItem"]] = relationship(back_populates="order", cascade="all, delete-orphan")

# class OrderItem(Base):
#     __tablename__ = "order_items"

#     id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
#     order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"), nullable=False)
#     product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False)
#     quantidade: Mapped[int] = mapped_column(Integer, nullable=False)
#     preco_unitario_no_pedido: Mapped[float] = mapped_column(Float, nullable=False) # Preço no momento da compra

#     order: Mapped["Order"] = relationship(back_populates="items")
#     product: Mapped["Product"] = relationship()