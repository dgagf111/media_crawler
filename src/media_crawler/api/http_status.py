from enum import Enum
from fastapi import status

class HTTPStatus(Enum):
    # =========== 成功状态 ===========
    SUCCESS = (status.HTTP_200_OK, "success")

    # =========== 服务器异常 ===========
    INTERNAL_SERVER_ERROR = (status.HTTP_500_INTERNAL_SERVER_ERROR, "internal server error")

    # =========== 客户端异常 ===========
    BAD_REQUEST = (status.HTTP_400_BAD_REQUEST, "bad request")
    UNAUTHORIZED = (status.HTTP_401_UNAUTHORIZED, "unauthorized")
    FORBIDDEN = (status.HTTP_403_FORBIDDEN, "forbidden")
    NOT_FOUND = (status.HTTP_404_NOT_FOUND, "not found")
    METHOD_NOT_ALLOWED = (status.HTTP_405_METHOD_NOT_ALLOWED, "method not allowed")

    def __init__(self, code, message):
        self._code = code
        self._message = message

    @property
    def code(self):
        return self._code
    
    @property
    def message(self):
        return self._message

