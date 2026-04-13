"""平台系列 API.

包含：模型列表
"""

from .._http import HTTPClient
from .._types import ModelListResponse


class PlatformAPI:
    """平台系列 API.

    包含平台相关接口，如模型列表.
    """

    def __init__(self, http: HTTPClient):
        """初始化平台 API 客户端.

        Args:
            http: HTTP 客户端实例
        """
        self._http = http

    async def list_models(self) -> ModelListResponse:
        """获取用户模型列表.

        Returns:
            可用模型列表
        """
        response = await self._http.get("models")
        return self._http.parse_json(response)
