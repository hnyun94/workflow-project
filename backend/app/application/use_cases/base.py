from abc import ABC, abstractmethod
from typing import Any, Dict

class UseCase(ABC):
    """기본 유스케이스"""
    
    @abstractmethod
    def execute(self, *args, **kwargs) -> Any:
        """유스케이스 실행"""
        pass

class UseCaseRequest(ABC):
    """유스케이스 요청"""
    pass

class UseCaseResponse(ABC):
    """유스케이스 응답"""
    pass

class SuccessResponse(UseCaseResponse):
    """성공 응답"""
    def __init__(self, data: Any = None, message: str = "Success"):
        self.data = data
        self.message = message
        self.success = True

class ErrorResponse(UseCaseResponse):
    """오류 응답"""
    def __init__(self, error: str, message: str = "Error occurred"):
        self.error = error
        self.message = message
        self.success = False
