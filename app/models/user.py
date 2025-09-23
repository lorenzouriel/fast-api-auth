from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.db.session import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), unique=True, index=True)
    phone_number = Column(String(15), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    password = Column(String(100))
    access_token = Column(String(2048))
    created_at = Column(DateTime, server_default=func.now())
    status = Column(Integer, default=1)

class UserSelection(Base):
    __tablename__ = "user_selections"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    stock_id = Column(Integer, ForeignKey("stocks.id"), nullable=True)
    crypto_id = Column(Integer, ForeignKey("cryptocurrencies.id"), nullable=True)
    currency_code = Column(String(10), ForeignKey("currencies.currency_code"), nullable=True)
    selected_at = Column(DateTime)
    created_at = Column(DateTime, server_default=func.now())
    status = Column(Integer, default=1)