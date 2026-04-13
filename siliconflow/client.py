"""SiliconFlow API 客户端.

提供统一的异步 API 客户端入口.
"""

from httpx import Limits, Timeout

from ._http import HTTPClient
from .api.audio import AudioAPI
from .api.batch import BatchAPI
from .api.image import ImageAPI
from .api.platform import PlatformAPI
from .api.text import TextAPI
from .api.video import VideoAPI


class SiliconFlowClient:
    """SiliconFlow API 异步客户端.

    提供命名空间方式访问各分类 API：
    - client.text: 文本系列 API（embeddings、chat、rerank）
    - client.image: 图像系列 API（generations）
    - client.audio: 语音系列 API（transcriptions、speech、voice）
    - client.video: 视频系列 API（generations）
    - client.batch: 批量处理 API（batch、files）
    - client.platform: 平台系列 API（models）

    Example:
        ```python
        from siliconflow import SiliconFlowClient

        client = SiliconFlowClient(key="your-api-key")

        # 文本嵌入
        result = await client.text.create_embed(
            model="BAAI/bge-m3",
            input="Hello, world!"
        )

        # 对话完成
        result = await client.text.chat_completions(
            model="Qwen/Qwen2.5-7B-Instruct",
            messages=[{"role": "user", "content": "Hello"}]
        )

        # 图片生成
        result = await client.image.generations(
            model="Kwai-Kolors/Kolors",
            prompt="a beautiful sunset"
        )
        ```
    """

    base_url: str = "https://api.siliconflow.cn/v1/"

    def __init__(
        self,
        key: str,
        base_url: str | None = None,
        timeout: float | Timeout = 60.0,
        limits: Limits | None = None,
    ):
        """初始化 SiliconFlow 客户端.

        Args:
            key: API Key
            base_url: API 基础 URL，默认 https://api.siliconflow.cn/v1/
            timeout: 请求超时时间（秒）或 Timeout 配置对象
            limits: 连接池限制配置
        """
        if isinstance(timeout, (int, float)):
            timeout = Timeout(timeout)

        self._http = HTTPClient(
            key=key,
            base_url=base_url or self.base_url,
            timeout=timeout,
            limits=limits,
        )

        # 初始化各分类 API 客户端
        self.text = TextAPI(self._http)
        self.image = ImageAPI(self._http)
        self.audio = AudioAPI(self._http)
        self.video = VideoAPI(self._http)
        self.batch = BatchAPI(self._http)
        self.platform = PlatformAPI(self._http)

    async def close(self) -> None:
        """关闭客户端连接池."""
        await self._http.close()

    async def __aenter__(self) -> "SiliconFlowClient":
        """异步上下文管理器入口."""
        return self

    async def __aexit__(self, *args) -> None:
        """异步上下文管理器退出."""
        await self.close()
