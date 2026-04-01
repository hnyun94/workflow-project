from abc import ABC, abstractmethod
from typing import List, Optional, Generic, TypeVar
from dataclasses import dataclass

T = TypeVar('T')

class Repository(ABC, Generic[T]):
    """기본 리포지토리 인터페이스"""
    
    @abstractmethod
    def get_by_id(self, id: int) -> Optional[T]:
        """ID로 엔티티 조회"""
        pass
    
    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> List[T]:
        """전체 엔티티 조회"""
        pass
    
    @abstractmethod
    def create(self, entity: T) -> T:
        """엔티티 생성"""
        pass
    
    @abstractmethod
    def update(self, entity: T) -> Optional[T]:
        """엔티티 업데이트"""
        pass
    
    @abstractmethod
    def delete(self, id: int) -> bool:
        """엔티티 삭제"""
        pass
    
    @abstractmethod
    def exists(self, id: int) -> bool:
        """엔티티 존재 여부 확인"""
        pass

@dataclass
class QueryParams:
    """쿼리 파라미터"""
    skip: int = 0
    limit: int = 100
    filters: dict = None
    
    def __post_init__(self):
        if self.filters is None:
            self.filters = {}
