from typing import Optional, Any
from pydantic import BaseModel


class ResponseDTO(BaseModel):
    success: bool
    data: Optional[Any] = None
    error: Optional[str] = None

    @classmethod
    def ok(cls, data: Any):
        return cls(success=True, data=data)

    @classmethod
    def fail(cls, error: str):
        return cls(success=False, error=error)