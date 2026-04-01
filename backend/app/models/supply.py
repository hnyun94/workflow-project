from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import enum

class TransactionType(enum.Enum):
    IN = "in"      # 입고
    OUT = "out"    # 출고
    RESERVE = "reserve"  # 예약

class SupplyStatus(enum.Enum):
    AVAILABLE = "available"
    OUT_OF_STOCK = "out_of_stock"
    RESERVED = "reserved"
    MAINTENANCE = "maintenance"

class SupplyCategory(Base):
    __tablename__ = "supply_categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    supplies = relationship("Supply", back_populates="category")

class Supply(Base):
    __tablename__ = "supplies"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    description = Column(Text)
    category_id = Column(Integer, ForeignKey("supply_categories.id"))
    quantity = Column(Integer, default=0)
    min_quantity = Column(Integer, default=1)  # 최소 재고량
    unit = Column(String, default="개")  # 단위
    location = Column(String)  # 보관 위치
    status = Column(String, default="available")  # 문자열로 변경
    price = Column(Numeric(10, 2))  # 단가
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    category = relationship("SupplyCategory", back_populates="supplies")
    transactions = relationship("SupplyTransaction", back_populates="supply")

class SupplyTransaction(Base):
    __tablename__ = "supply_transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    supply_id = Column(Integer, ForeignKey("supplies.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    transaction_type = Column(Enum(TransactionType))
    quantity = Column(Integer, nullable=False)
    quantity_before = Column(Integer)  # 거래 전 수량
    quantity_after = Column(Integer)   # 거래 후 수량
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    supply = relationship("Supply", back_populates="transactions")
    user = relationship("User")
