from sqlalchemy import Column, Integer, String, Float, Date, Boolean, ARRAY
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    descricao = Column(String, nullable=False)
    valor_venda = Column(Float, nullable=False)
    codigo_barras = Column(String, unique=True, nullable=False)
    secao = Column(String, nullable=True)
    estoque_inicial = Column(Integer, default=0)
    data_validade = Column(Date, nullable=True)
    disponivel = Column(Boolean, default=True)
    # Para armazenar URLs das imagens, pode usar ARRAY se usar PostgreSQL, ou um relacionamento separado
    imagens = Column(ARRAY(String), nullable=True)  # ajuste se usar outro banco
