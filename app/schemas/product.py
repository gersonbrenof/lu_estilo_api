from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date

# Base comum para entrada e saída
class ProductBase(BaseModel):
    descricao: str = Field(..., example="Sabonete Líquido 500ml")
    valor_venda: float = Field(..., example=15.99)
    codigo_barras: str = Field(..., example="7891234567890")
    secao: Optional[str] = Field(None, example="Higiene")
    estoque_inicial: int = Field(0, example=100)
    data_validade: Optional[date] = Field(None, example="2025-12-31")
    disponivel: bool = Field(True, example=True)

# Usado na criação de um novo produto
class ProductCreate(ProductBase):
    pass

# Usado na atualização de um produto existente
class ProductUpdate(ProductBase):
    pass

# Retorno da API, com ID incluído
class ProductOut(ProductBase):
    id: int

    class Config:
        orm_mode = True
