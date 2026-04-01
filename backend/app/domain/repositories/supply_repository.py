from typing import List, Optional
from .base import Repository
from ..entities.supply import Supply, SupplyCategory
from ..enums.common import SupplyStatus

class SupplyRepository(Repository[Supply]):
    """비품 리포지토리 인터페이스"""
    
    @abstractmethod
    def get_by_category(self, category_id: int) -> List[Supply]:
        """카테고리별 비품 조회"""
        pass
    
    @abstractmethod
    def get_by_status(self, status: SupplyStatus) -> List[Supply]:
        """상태별 비품 조회"""
        pass
    
    @abstractmethod
    def get_low_stock_supplies(self) -> List[Supply]:
        """재고 부족 비품 조회"""
        pass
    
    @abstractmethod
    def get_available_supplies(self) -> List[Supply]:
        """사용 가능한 비품 조회"""
        pass
    
    @abstractmethod
    def search_by_name(self, name: str) -> List[Supply]:
        """이름으로 비품 검색"""
        pass
    
    @abstractmethod
    def update_quantity(self, supply_id: int, new_quantity: int) -> Optional[Supply]:
        """수량 업데이트"""
        pass

class SupplyCategoryRepository(Repository[SupplyCategory]):
    """비품 카테고리 리포지토리 인터페이스"""
    
    @abstractmethod
    def get_by_name(self, name: str) -> Optional[SupplyCategory]:
        """이름으로 카테고리 조회"""
        pass
    
    @abstractmethod
    def name_exists(self, name: str) -> bool:
        """카테고리 이름 중복 확인"""
        pass
    
    @abstractmethod
    def get_with_supplies_count(self) -> List[dict]:
        """비품 수 포함 카테고리 조회"""
        pass
