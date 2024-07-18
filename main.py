# main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Dict
from contextlib import asynccontextmanager
from models import Order as ORMOrder, OrderDetail as ORMOrderDetail, SessionLocal, init_models


class Order(BaseModel):
    id: int
    date: str
    amount: int
    method: str
    customer: str


class OrderDetail(BaseModel):
    id: int
    date: str
    product: int
    quantity: int
    subtotal: int


# 데이터베이스 세션 의존성
async def get_db():
    async with SessionLocal() as db:
        try:
            yield db
        finally:
            await db.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_models()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/orders/")
async def post_orders(data: Dict[str, List[Dict]], db: Session = Depends(get_db)):
    orders = []
    details = []

    if 'orders' in data:
        for item in data['orders']:
            order = Order(**item)
            orders.append(order)

    if 'details' in data:
        for item in data['details']:
            detail = OrderDetail(**item)
            details.append(detail)

    try:
        for order in orders:
            db_order = ORMOrder(**order.dict())
            db.add(db_order)

        for detail in details:
            db_detail = ORMOrderDetail(**detail.dict())
            db.add(db_detail)

        await db.commit()
    except Exception as e:
        await db.rollback()
        if "1062" in str(e):  # MySQL 오류 코드 1062: Duplicate entry
            raise HTTPException(status_code=400, detail="Duplicate entry detected")
        else:
            raise HTTPException(status_code=500, detail=str(e))

    return {"message": "Orders and details successfully inserted"}


# FastAPI 서버 실행 (uvicorn으로 실행)
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8081, reload=True)
