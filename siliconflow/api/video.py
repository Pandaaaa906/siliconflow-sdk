"""视频系列 API.

包含：视频生成、视频状态查询
"""

from typing import Any

from .._http import HTTPClient
from .._types import VideoGenerationResponse


class VideoAPI:
    """视频系列 API.

    包含视频生成相关接口.
    """

    def __init__(self, http: HTTPClient):
        """初始化视频 API 客户端.

        Args:
            http: HTTP 客户端实例
        """
        self._http = http

    async def generations(
        self,
        model: str,
        prompt: str,
        seed: int | None = None,
        image: str | None = None,
        duration: int | None = None,
        resolution: str | None = None,
    ) -> VideoGenerationResponse:
        """创建视频生成请求.

        Args:
            model: 模型名称
            prompt: 视频描述文本
            seed: 随机种子
            image: 首帧图片 URL 或 base64
            duration: 视频时长（秒）
            resolution: 视频分辨率

        Returns:
            视频生成响应，包含任务 ID
        """
        payload: dict[str, Any] = {
            "model": model,
            "prompt": prompt,
        }

        if seed is not None:
            payload["seed"] = seed
        if image is not None:
            payload["image"] = image
        if duration is not None:
            payload["duration"] = duration
        if resolution is not None:
            payload["resolution"] = resolution

        response = await self._http.post("video/generations", json=payload)
        return self._http.parse_json(response)

    async def get_generation(self, id: str) -> VideoGenerationResponse:
        """获取视频生成任务状态.

        Args:
            id: 视频生成任务 ID

        Returns:
            视频生成任务状态和结果
        """
        response = await self._http.get(f"video/generations/{id}")
        return self._http.parse_json(response)
