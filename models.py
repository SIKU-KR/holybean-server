# models.py
from sqlalchemy import Column, Integer, String, Date, create_engine, UniqueConstraint, PrimaryKeyConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URL

# DATABASE_URL을 config.py에서 가져와서 사용
engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)
Base = declarative_base()


class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, nullable=False)
    date = Column(Date, nullable=False)
    amount = Column(Integer)
    method = Column(String(50))
    customer = Column(String(50))
    __table_args__ = (
        PrimaryKeyConstraint('id', 'date', name='pk_order_id_date'),
    )


class OrderDetail(Base):
    __tablename__ = "order_details"
    id = Column(Integer, nullable=False)
    date = Column(Date, nullable=False)
    product = Column(Integer)
    quantity = Column(Integer)
    subtotal = Column(Integer)
    __table_args__ = (
        PrimaryKeyConstraint('id', 'date', name='pk_order_detail_id_date'),
    )


# 테이블 생성 (비동기로 변경)
async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# main.py에서 호출할 수 있도록 설정
init_models()
