"""批量处理 API.

包含：batch 任务管理、文件上传
"""

from typing import Any, BinaryIO

from .._http import HTTPClient
from .._types import (
    Batch,
    BatchListResponse,
    FileListResponse,
    FileUploadResponse,
)


class BatchAPI:
    """批量处理 API.

    包含 batch 任务管理和文件上传相关接口.
    """

    def __init__(self, http: HTTPClient):
        """初始化批量处理 API 客户端.

        Args:
            http: HTTP 客户端实例
        """
        self._http = http

    async def create(
        self,
        input_file_id: str,
        endpoint: str,
        completion_window: str = "24h",
        metadata: dict[str, str] | None = None,
    ) -> Batch:
        """创建 batch 任务.

        Args:
            input_file_id: 输入文件 ID
            endpoint: 目标端点，如 /v1/chat/completions
            completion_window: 完成窗口，默认 "24h"
            metadata: 自定义元数据

        Returns:
            创建的 batch 任务信息
        """
        payload: dict[str, Any] = {
            "input_file_id": input_file_id,
            "endpoint": endpoint,
            "completion_window": completion_window,
        }

        if metadata is not None:
            payload["metadata"] = metadata

        response = await self._http.post("batch", json=payload)
        return self._http.parse_json(response)

    async def list(self, limit: int | None = None, after: str | None = None) -> BatchListResponse:
        """获取 batch 任务列表.

        Args:
            limit: 返回数量限制
            after: 分页游标

        Returns:
            batch 任务列表
        """
        params: dict[str, Any] = {}
        if limit is not None:
            params["limit"] = limit
        if after is not None:
            params["after"] = after

        response = await self._http.get("batch", params=params if params else None)
        return self._http.parse_json(response)

    async def get(self, id: str) -> Batch:
        """获取 batch 任务详情.

        Args:
            id: batch 任务 ID

        Returns:
            batch 任务详情
        """
        response = await self._http.get(f"batch/{id}")
        return self._http.parse_json(response)

    async def cancel(self, id: str) -> Batch:
        """取消 batch 任务.

        Args:
            id: batch 任务 ID

        Returns:
            更新后的 batch 任务信息
        """
        response = await self._http.post(f"batch/{id}/cancel", json={})
        return self._http.parse_json(response)

    async def upload_file(
        self,
        file: BinaryIO,
        purpose: str = "batch",
    ) -> FileUploadResponse:
        """上传文件.

        Args:
            file: 文件对象
            purpose: 文件用途，默认 "batch"

        Returns:
            上传的文件信息
        """
        files = {
            "file": file,
        }
        data = {
            "purpose": purpose,
        }

        response = await self._http.post_form("files", data=data, files=files)
        return self._http.parse_json(response)

    async def list_files(
        self,
        purpose: str | None = None,
        limit: int | None = None,
    ) -> FileListResponse:
        """获取文件列表.

        Args:
            purpose: 按用途筛选
            limit: 返回数量限制

        Returns:
            文件列表
        """
        params: dict[str, Any] = {}
        if purpose is not None:
            params["purpose"] = purpose
        if limit is not None:
            params["limit"] = limit

        response = await self._http.get("files", params=params if params else None)
        return self._http.parse_json(response)
