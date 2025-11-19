from typing import Generic, TypeVar, Optional, Any
from pydantic import BaseModel, Field
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from pythonprojecttemplate.api.http_status import HTTPStatus

T = TypeVar('T')

class ResultVO(BaseModel, Generic[T]):
    code: int = Field(default=200, description="code")
    message: str = Field(default="success", description="message")
    data: Optional[T] = Field(default=None, description="data")

    def to_response(self) -> JSONResponse:  
        content = jsonable_encoder(self.model_dump())
        return JSONResponse(content=content, status_code=self.code)

    @classmethod    
    def success(cls, data: Optional[T] = None, 
                message: str = HTTPStatus.SUCCESS.message,
                status_code: int = HTTPStatus.SUCCESS.code) -> JSONResponse:
        return cls(code=status_code, message=message, data=data).to_response()

    @classmethod
    def error(cls, code: int = HTTPStatus.INTERNAL_SERVER_ERROR.code,
               message: str = HTTPStatus.INTERNAL_SERVER_ERROR.message) -> JSONResponse:
        return cls(code=code, message=message, data=None).to_response()

# 示例使用
# result = ResultVO.success(data={"key": "value"})
# 直接返回 result，它已经是一个 JSONResponse 对象