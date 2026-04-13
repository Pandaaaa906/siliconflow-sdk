"""SiliconFlow API HTTP 客户端.

封装 httpx.AsyncClient，提供统一的 HTTP 请求接口.
"""

from typing import Any

import httpx
import orjson
from httpx import Limits, Response, Timeout


def _orjson_dumps(obj: Any) -> str:
    """使用 orjson 序列化为字符串."""
    return orjson.dumps(obj).decode("utf-8")


class HTTPClient:
    """SiliconFlow API HTTP 客户端.

    封装 httpx.AsyncClient，提供：
    - 自动认证（Bearer Token）
    - 自动 URL 拼接
    - orjson 序列化/反序列化
    - 连接池和超时配置
    """

    def __init__(
        self,
        key: str,
        base_url: str = "https://api.siliconflow.cn/v1/",
        timeout: Timeout | None = None,
        limits: Limits | None = None,
        client: httpx.AsyncClient | None = None,
    ):
        """初始化 HTTP 客户端.

        Args:
            key: API Key
            base_url: API 基础 URL
            timeout: 请求超时配置
            limits: 连接池限制配置
            client: 自定义 httpx.AsyncClient 实例
        """
        self.base_url = base_url.rstrip("/") + "/"

        if client is None:
            if timeout is None:
                timeout = Timeout(60.0)
            if limits is None:
                limits = Limits(max_connections=200, max_keepalive_connections=50)
            client = httpx.AsyncClient(timeout=timeout, limits=limits)

        client.headers.update({
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
        })
        self._client = client

    async def post(
        self,
        url: str,
        json: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> Response:
        """发送 POST 请求.

        Args:
            url: 相对 URL 路径
            json: JSON 请求体
            **kwargs: 传递给 httpx 的其他参数

        Returns:
            HTTP 响应对象
        """
        full_url = self.base_url + url.lstrip("/")

        if json is not None and "content" not in kwargs:
            kwargs["content"] = orjson.dumps(json)
            kwargs["headers"] = {**kwargs.get("headers", {}), "Content-Type": "application/json"}

        response = await self._client.post(full_url, **kwargs)
        response.raise_for_status()
        return response

    async def get(self, url: str, **kwargs: Any) -> Response:
        """发送 GET 请求.

        Args:
            url: 相对 URL 路径
            **kwargs: 传递给 httpx 的其他参数

        Returns:
            HTTP 响应对象
        """
        full_url = self.base_url + url.lstrip("/")
        response = await self._client.get(full_url, **kwargs)
        response.raise_for_status()
        return response

    async def delete(self, url: str, **kwargs: Any) -> Response:
        """发送 DELETE 请求.

        Args:
            url: 相对 URL 路径
            **kwargs: 传递给 httpx 的其他参数

        Returns:
            HTTP 响应对象
        """
        full_url = self.base_url + url.lstrip("/")
        response = await self._client.delete(full_url, **kwargs)
        response.raise_for_status()
        return response

    async def post_form(
        self,
        url: str,
        data: dict[str, Any] | None = None,
        files: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> Response:
        """发送 multipart/form-data POST 请求（用于文件上传）.

        Args:
            url: 相对 URL 路径
            data: 表单数据
            files: 文件数据
            **kwargs: 传递给 httpx 的其他参数

        Returns:
            HTTP 响应对象
        """
        full_url = self.base_url + url.lstrip("/")

        # 移除 Content-Type，让 httpx 自动设置 multipart boundary
        headers = {k: v for k, v in kwargs.pop("headers", {}).items() if k.lower() != "content-type"}

        response = await self._client.post(
            full_url,
            data=data,
            files=files,
            headers=headers,
            **kwargs,
        )
        response.raise_for_status()
        return response

    def parse_json(self, response: Response) -> Any:
        """使用 orjson 解析响应 JSON.

        Args:
            response: HTTP 响应对象

        Returns:
            解析后的 Python 对象
        """
        return orjson.loads(response.content)

    async def close(self) -> None:
        """关闭 HTTP 客户端连接池."""
        await self._client.aclose()

    async def __aenter__(self) -> "HTTPClient":
        """异步上下文管理器入口."""
        return self

    async def __aexit__(self, *args: Any) -> None:
        """异步上下文管理器退出."""
        await self.close()
