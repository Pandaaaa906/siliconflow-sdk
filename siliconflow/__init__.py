"""SiliconFlow API Python SDK.

一个异步的 SiliconFlow API 客户端，支持：
- 文本系列：embeddings、chat completions、rerank
- 图像系列：image generations
- 语音系列：transcriptions、speech、voice management
- 视频系列：video generations
- 批量处理：batch、files
- 平台系列：models

Example:
    ```python
    from siliconflow import SiliconFlowClient

    async with SiliconFlowClient(key="your-api-key") as client:
        # 文本嵌入
        result = await client.text.create_embed(
            model="BAAI/bge-m3",
            input="Hello, world!"
        )
        print(result["data"][0]["embedding"])

        # 对话完成
        result = await client.text.chat_completions(
            model="Qwen/Qwen2.5-7B-Instruct",
            messages=[{"role": "user", "content": "Hello"}]
        )
        print(result["choices"][0]["message"]["content"])
    ```
"""

from .client import SiliconFlowClient

__all__ = ["SiliconFlowClient"]
__version__ = "0.1.0"
