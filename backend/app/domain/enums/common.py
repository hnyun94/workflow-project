from enum import Enum

class UserRole(Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    USER = "user"

class SupplyStatus(Enum):
    AVAILABLE = "available"
    OUT_OF_STOCK = "out_of_stock"
    RESERVED = "reserved"
    MAINTENANCE = "maintenance"

class TransactionType(Enum):
    IN = "in"
    OUT = "out"
    RESERVE = "reserve"

class ReservationStatus(Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
