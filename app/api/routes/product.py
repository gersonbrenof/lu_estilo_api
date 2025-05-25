from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.product import ProductCreate, ProductOut, ProductUpdate
from app.crud import product as crud
from typing import List, Optional
from app.models.product import Product
from app.api.dependencies import  check_user_role# Ajuste o nome conforme o módulo
from app.api.dependencies import get_current_user, check_user_role
from app.models.user import User

product = APIRouter()

@product.get("/products", response_model=List[ProductOut])
def listar_produtos(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=100),
    secao: Optional[str] = Query(None),
    preco_min: Optional[float] = Query(None),
    preco_max: Optional[float] = Query(None),
    disponivel: Optional[bool] = Query(None),
    current_user: User = Depends(get_current_user)
):
    """
    Lista produtos com suporte a filtros e paginação.
    """
    query = db.query(Product)

    if secao:
        query = query.filter(Product.secao.ilike(f"%{secao}%"))

    if preco_min is not None:
        query = query.filter(Product.valor_venda >= preco_min)

    if preco_max is not None:
        query = query.filter(Product.valor_venda <= preco_max)

    if disponivel is not None:
        query = query.filter(Product.disponivel == disponivel)

    produtos = query.offset(skip).limit(limit).all()
    return produtos

@product.get("/products/{product_id}", response_model=ProductOut)
def get_product(product_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    product = crud.get_product_by_id(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return product

@product.post("/products", response_model=ProductOut)
def create_product(product: ProductCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    check_user_role(current_user)
    return crud.create_product(db, product)

@product.put("/{product_id}", response_model=ProductOut)
def update_product(product_id: int, product_data: ProductUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    updated = crud.update_product(db, product_id, product_data)
    check_user_role(current_user)
    if not updated:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return updated

@product.delete("/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    check_user_role(current_user)
    deleted = crud.delete_product(db, product_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return