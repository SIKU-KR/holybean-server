# models.py
from sqlalchemy import Column, Integer, String, Date, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URL

# DATABASE_URL을 config.py에서 가져와서 사용
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date)
    amount = Column(Integer)
    method = Column(String(50))
    customer = Column(String(50))

class OrderDetail(Base):
    __tablename__ = "order_details"
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date)
    product = Column(Integer)
    quantity = Column(Integer)
    subtotal = Column(Integer)

# 테이블 생성
Base.metadata.create_all(bind=engine)
