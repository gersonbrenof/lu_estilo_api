from sqlalchemy import Column, Integer, String, ForeignKey
from app.core.database import Base
from sqlalchemy.orm import relationship
class Client(Base):
    __tablename__ = "clients"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    cpf = Column(String, unique=True, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    user = relationship("User", back_populates="client")
    pedidos = relationship("Pedido", back_populates="cliente")