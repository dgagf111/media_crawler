from fastapi import APIRouter, Depends, Body
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from .auth.auth_service import authenticate_user, get_current_user, get_db, get_current_app
from .auth.token_service import create_tokens, refresh_access_token, revoke_tokens, generate_permanent_token
from pythonprojecttemplate.api.models.token_response_model import TokenResponse
from pythonprojecttemplate.api.models.auth_models import User
from pythonprojecttemplate.config.settings import settings
from pythonprojecttemplate.log.logHelper import get_logger
from pythonprojecttemplate.api.exception.custom_exceptions import (
    APIException,
    IncorrectCredentialsException,
    InvalidCredentialsException,
    InvalidTokenException,
    TokenRevokedException,
)
from pythonprojecttemplate.api.models.result_vo import ResultVO
from pythonprojecttemplate.api.http_status import HTTPStatus
from media_crawler.api.spider_xhs_router import router as spider_xhs_router
from media_crawler.api.xhs_downloader_router import router as xhs_downloader_router

logger = get_logger()

# 缓存 API 版本，避免重复调用
API_VERSION = settings.common.api_version
API_PREFIX = f"/api/{API_VERSION}"

api_router = APIRouter(prefix=API_PREFIX)


def _build_token_response(tokens: dict) -> TokenResponse:
    return TokenResponse(
        access_token=tokens["access_token"],
        token_type=tokens.get("token_type", "bearer"),
        refresh_token=tokens["refresh_token"],
    )

#######################
# 实际使用的生产接口 #
#######################

@api_router.post("/token")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_db)
):
    """用户登录并获取访问令牌

    此接口用于用户登录并获取访问令牌和刷新令牌。

    Args:
        form_data: 包含用户名和密码的表单数据
        session: 异步数据库会话

    Returns:
        ResultVO: 成功时包含访问令牌和刷新令牌

    Raises:
        InvalidCredentialsException: 用户名或密码不正确
    """
    try:
        # authenticate_user 现在会抛出异常或返回 tokens
        tokens = await authenticate_user(session, form_data.username, form_data.password)

        if not tokens:
            raise InvalidCredentialsException(detail="用户名或密码不正确")

        logger.info(f"用户登录成功: {form_data.username}")
        return ResultVO.success(
            data=_build_token_response(tokens),
            message="登录成功"
        )
    except (InvalidCredentialsException, IncorrectCredentialsException) as e:
        logger.warning(f"登录失败: {form_data.username}, 原因: {e.detail}")
        return ResultVO.error(
            code=HTTPStatus.UNAUTHORIZED.code,
            message=e.detail or "用户名或密码不正确"
        )
    except Exception as e:
        logger.error(f"登录时发生未知错误: {form_data.username}", exc_info=True)
        return ResultVO.error(
            code=HTTPStatus.INTERNAL_SERVER_ERROR.code,
            message="登录失败，请稍后重试"
        )

REFRESH_TOKEN_INVALID_MESSAGE = "刷新令牌无效或已过期，请重新登录"


@api_router.post("/refresh")
async def refresh_token(refresh_token: str = Body(..., embed=True)):
    """
    刷新访问令牌
    
    此接口用于使用刷新令牌获取新的访问令牌和刷新令牌。
    
    参数:
    - refresh_token (str): 用于刷新的令牌
    
    返回:
    - 成功: ResultVO对象,包含以下数据:
        - code (int): 状态码
        - message (str): 成功消息
        - data (dict): 包含以下字段:
            - access_token (str): 新的访问令牌
            - token_type (str): 令牌类型,固定为"bearer"
            - refresh_token (str): 新的刷新令牌
    - 失败: ResultVO对象,包含以下数据:
        - code (int): 错误码
        - message (str): 错误信息
        - data (None): 失败时data为空
    
    异常:
    - InvalidTokenException: 令牌类型无效
    - 其他异常: 记录到日志并返回通用错误信息
    """
    try:
        new_access_token, new_refresh_token = refresh_access_token(refresh_token)
        token_response = TokenResponse(
            access_token=new_access_token,
            token_type="bearer",
            refresh_token=new_refresh_token,
        )
        return ResultVO.success(data=token_response)
    except (InvalidTokenException, TokenRevokedException) as exc:
        logger.warning("刷新令牌失败: %s", exc.detail)
        return ResultVO.error(code=HTTPStatus.UNAUTHORIZED.code, message=REFRESH_TOKEN_INVALID_MESSAGE)
    except APIException as exc:
        logger.warning("刷新令牌发生业务异常: %s", exc.detail)
        status_code = getattr(exc, "status_code", HTTPStatus.INTERNAL_SERVER_ERROR.code)
        return ResultVO.error(code=status_code, message=str(exc.detail))
    except Exception:
        logger.error("刷新令牌出现未知错误", exc_info=True)
        return ResultVO.error(
            code=HTTPStatus.INTERNAL_SERVER_ERROR.code,
            message="刷新令牌失败，请稍后重试",
        )

@api_router.post("/logout")
async def logout(current_user: User = Depends(get_current_user)):
    """
    用户登出
    
    此接口用于用户登出,会撤销用户的所有令牌。
    
    认证:
    - 此接口需要认证。请在请求头中提供有效的Bearer Token。
    - 格式: Authorization: Bearer <access_token>
    - 系统会自动验证token并获取对应的用户信息,无需在请求体中额外提供用户信息。
    
    参数:
    - current_user (User): 当前登录的用户对象。此参数由系统根据提供的token自动注入,包含以下字段:
        - username (str): 用户名
        - user_id (int): 用户ID
        - email (str): 用户邮箱
        - ... (其他用户模型中定义的字段)
    
    返回:
    - 成功: ResultVO对象,包含以下数据:
        - code (int): 状态码
        - message (str): 成功消息
        - data (None): 登出成功时data为空
    - 失败: ResultVO对象,包含以下数据:
        - code (int): 错误码
        - message (str): 错误信息
        - data (None): 失败时data为空
    
    异常:
    - 401 Unauthorized: 如果提供的token无效或已过期
    - 404 Not Found: 如果token对应的用户不存在
    - 500 Internal Server Error: 服务器内部错误
    
    注意:
    - 调用此接口会使当前用户的所有有效token失效,包括其他设备上的登录状态。
    """
    try:
        revoke_tokens(current_user.username)
        return ResultVO.success(message="Successfully logged out")
    except Exception as e:
        logger.error(f"Error logging out: {str(e)}")
        return ResultVO.error(code=HTTPStatus.INTERNAL_SERVER_ERROR.code, message="Failed to log out")

@api_router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), session: AsyncSession = Depends(get_db)):
    """用户登录

    此接口用于用户登录并获取访问令牌和刷新令牌。

    参数:
    - form_data (OAuth2PasswordRequestForm): 包含以下字段的表单数据:
        - username (str): 用户名
        - password (str): 密码
    - session (AsyncSession): 异步数据库会话对象

    返回:
    - 成功: ResultVO对象,包含以下数据:
        - code (int): 状态码
        - message (str): 成功消息
        - data (dict): 包含以下字段:
            - access_token (str): 访问令牌
            - refresh_token (str): 刷新令牌
            - token_type (str): 令牌类型,固定为"bearer"
    - 失败: ResultVO对象,包含以下数据:
        - code (int): 错误码
        - message (str): 错误信息
        - data (None): 失败时data为空

    异常:
    - IncorrectCredentialsException: 用户名或密码不正确
    - 其他异常: 记录到日志并返回通用错误信息
    """
    try:
        tokens = await authenticate_user(session, form_data.username, form_data.password)
        if not tokens:
            raise IncorrectCredentialsException(detail="Incorrect username or password")
        return ResultVO.success(data=_build_token_response(tokens))
    except (InvalidCredentialsException, IncorrectCredentialsException) as exc:
        logger.warning(f"登录失败: {form_data.username}, 原因: {exc.detail}")
        return ResultVO.error(
            code=HTTPStatus.UNAUTHORIZED.code,
            message=exc.detail or "Invalid credentials"
        )
    except Exception as e:
        logger.error(f"Error logging in: {str(e)}", exc_info=True)
        return ResultVO.error(code=HTTPStatus.INTERNAL_SERVER_ERROR.code, message="Invalid credentials")

@api_router.post("/generate_permanent_token")
async def generate_token(
    user_id: int,
    provider: str,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    """生成永久令牌

    此接口用于生成长期有效的令牌,通常用于第三方应用或服务集成。

    参数:
    - user_id (int): 用户ID
    - provider (str): 提供者信息,用于标识令牌的来源或用途
    - session (AsyncSession): 异步数据库会话对象

    返回:
    - 成功: ResultVO对象,包含以下数据:
        - code (int): 状态码
        - message (str): 成功消息
        - data (dict): 包含以下字段:
            - permanent_token (str): 生成的永久令牌
    - 失败: ResultVO对象,包含以下数据:
        - code (int): 错误码
        - message (str): 错误信息
        - data (None): 失败时data为空
    """
    try:
        if current_user.user_id != user_id:
            return ResultVO.error(
                code=HTTPStatus.FORBIDDEN.code,
                message="Forbidden: mismatched user_id"
            )

        token = await generate_permanent_token(session, user_id, provider)
        return ResultVO.success(data={"permanent_token": token})
    except Exception as e:
        logger.error(f"Error generating permanent token: {str(e)}")
        return ResultVO.error(code=HTTPStatus.INTERNAL_SERVER_ERROR.code, message="Failed to generate permanent token")

#######################
#     测试用接口     #
#######################

@api_router.get("/test")
async def test_route(current_user: User = Depends(get_current_user)):
    try:
        return ResultVO.success(data={"message": "Test route", "version": API_VERSION, "user": current_user.username})
    except Exception as e:
        logger.error(f"Error testing route: {str(e)}")
        return ResultVO.error(code=HTTPStatus.INTERNAL_SERVER_ERROR.code, message="Failed to test route")

@api_router.get("/third_party_test")
async def third_party_test(current_app: str = Depends(get_current_app)):
    try:
        return ResultVO.success(data={"app": current_app}, message="Third party access successful")
    except Exception as e:
        logger.error(f"Error testing third party access: {str(e)}")
        return ResultVO.error(code=HTTPStatus.INTERNAL_SERVER_ERROR.code, message="Failed to test third party access")

@api_router.get("/test_exception")
async def test_exception_route():
    raise APIException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR.code, detail="测试异常")


api_router.include_router(spider_xhs_router)
api_router.include_router(xhs_downloader_router)
