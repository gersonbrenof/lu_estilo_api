# from pydantic import BaseModel, Field
# from typing import List, Optional
# from datetime import datetime
# from app.models.order import OrderStatus # Importar o Enum do modelo
# from .product import Product # Para exibir detalhes do produto no item do pedido

# # --- OrderItem Schemas ---
# class OrderItemBase(BaseModel):
#     product_id: int
#     quantidade: int = Field(gt=0)

# class OrderItemCreate(OrderItemBase):
#     # O preço unitário será pego do produto no momento da criação do pedido
#     pass

# class OrderItemUpdate(BaseModel): # Atualizar item de um pedido existente
#     quantidade: Optional[int] = Field(default=None, gt=0)
#     # Não permitir mudar product_id ou preço aqui, remova o item e adicione um novo

# class OrderItem(OrderItemBase): # Para exibir em um pedido
#     id: int
#     preco_unitario_no_pedido: float
#     product: Optional[Product] = None # Para mostrar detalhes do produto

#     class Config:
#         orm_mode = True

# # --- Order Schemas ---
# class OrderBase(BaseModel):
#     client_id: int

# class OrderCreate(OrderBase):
#     items: List[OrderItemCreate]

# class OrderUpdate(BaseModel): # O que pode ser atualizado em um pedido
#     status: Optional[OrderStatus] = None
#     # Adicionar/remover itens seria uma lógica mais complexa,
#     # talvez rotas dedicadas /orders/{order_id}/items
#     # items_to_add: Optional[List[OrderItemCreate]] = None
#     # item_ids_to_remove: Optional[List[int]] = None
#     # items_to_update: Optional[List[Tuple[int, OrderItemUpdate]]] = None # (item_id, update_data)


# class OrderInDBBase(OrderBase):
#     id: int
#     status: OrderStatus
#     created_at: datetime
#     updated_at: datetime
#     items: List[OrderItem] = []
#     # total_amount: Optional[float] = None # Calcular no backend

#     class Config:
#         orm_mode = True

# class Order(OrderInDBBase): # Para respostas da API
#     pass

# class OrderInDB(OrderInDBBase): # Para uso interno
#     pass