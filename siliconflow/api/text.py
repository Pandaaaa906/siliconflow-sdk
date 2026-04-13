"""文本系列 API.

包含：embeddings、chat completions、rerank
"""

from typing import Any, AsyncIterator

from .._http import HTTPClient
from .._types import (
    ChatCompletionResponse,
    ChatCompletionStreamResponse,
    EmbeddingResponse,
    Message,
    RerankResponse,
)


class TextAPI:
    """文本系列 API.

    包含 embeddings、chat completions、rerank 等文本相关接口.
    """

    def __init__(self, http: HTTPClient):
        """初始化文本 API 客户端.

        Args:
            http: HTTP 客户端实例
        """
        self._http = http

    async def create_embed(
        self,
        model: str,
        input: str | list[str],
        encoding_format: str = "float",
        dimensions: int | None = None,
    ) -> EmbeddingResponse:
        """创建文本嵌入向量.

        Args:
            model: 模型名称，如 "BAAI/bge-m3"
            input: 输入文本，可为字符串或字符串数组（最多32项）
            encoding_format: 返回格式，"float" 或 "base64"
            dimensions: 输出维度，仅 Qwen3 系列支持

        Returns:
            嵌入响应，包含 embedding 向量和 token 使用情况

        Raises:
            httpx.HTTPError: 请求失败时抛出
        """
        payload: dict[str, Any] = {
            "model": model,
            "input": input,
            "encoding_format": encoding_format,
        }
        if dimensions is not None:
            payload["dimensions"] = dimensions

        response = await self._http.post("embeddings", json=payload)
        return self._http.parse_json(response)

    async def chat_completions(
        self,
        model: str,
        messages: list[Message],
        stream: bool = False,
        max_tokens: int | None = None,
        temperature: float | None = None,
        top_p: float | None = None,
        top_k: int | None = None,
        frequency_penalty: float | None = None,
        stop: str | list[str] | None = None,
        n: int = 1,
        response_format: dict[str, Any] | None = None,
        tools: list[dict[str, Any]] | None = None,
        enable_thinking: bool | None = None,
        thinking_budget: int | None = None,
        min_p: float | None = None,
    ) -> ChatCompletionResponse | AsyncIterator[ChatCompletionStreamResponse]:
        """创建对话完成请求.

        Args:
            model: 模型名称
            messages: 对话消息列表
            stream: 是否流式返回
            max_tokens: 最大生成 token 数
            temperature: 随机性控制 (0-2)
            top_p: 核采样阈值 (0-1)
            top_k: Top-k 采样
            frequency_penalty: 频率惩罚 (-2 到 2)
            stop: 停止序列，最多4个
            n: 生成数量
            response_format: 输出格式配置
            tools: 可用工具列表
            enable_thinking: 是否启用思考模式
            thinking_budget: 最大推理 token 数 (128-32768)
            min_p: 动态过滤阈值 (0-1，仅 Qwen3)

        Returns:
            对话完成响应或流式响应迭代器
        """
        payload: dict[str, Any] = {
            "model": model,
            "messages": messages,
            "stream": stream,
            "n": n,
        }

        if max_tokens is not None:
            payload["max_tokens"] = max_tokens
        if temperature is not None:
            payload["temperature"] = temperature
        if top_p is not None:
            payload["top_p"] = top_p
        if top_k is not None:
            payload["top_k"] = top_k
        if frequency_penalty is not None:
            payload["frequency_penalty"] = frequency_penalty
        if stop is not None:
            payload["stop"] = stop
        if response_format is not None:
            payload["response_format"] = response_format
        if tools is not None:
            payload["tools"] = tools
        if enable_thinking is not None:
            payload["enable_thinking"] = enable_thinking
        if thinking_budget is not None:
            payload["thinking_budget"] = thinking_budget
        if min_p is not None:
            payload["min_p"] = min_p

        if stream:
            return self._chat_completions_stream(payload)

        response = await self._http.post("chat/completions", json=payload)
        return self._http.parse_json(response)

    async def _chat_completions_stream(
        self,
        payload: dict[str, Any],
    ) -> AsyncIterator[ChatCompletionStreamResponse]:
        """处理流式对话完成请求.

        Args:
            payload: 请求体

        Yields:
            流式响应块
        """
        full_url = self._http.base_url + "chat/completions"

        async with self._http._client.stream(
            "POST",
            full_url,
            content=__import__("orjson").dumps(payload),
            headers={"Content-Type": "application/json"},
        ) as response:
            response.raise_for_status()
            async for line in response.aiter_lines():
                if line.startswith("data: "):
                    data = line[6:]
                    if data == "[DONE]":
                        break
                    yield __import__("orjson").loads(data)

    async def chat_completions_anthropic(
        self,
        model: str,
        messages: list[Message],
        stream: bool = False,
        max_tokens: int | None = None,
        temperature: float | None = None,
        top_p: float | None = None,
        top_k: int | None = None,
        stop: str | list[str] | None = None,
    ) -> ChatCompletionResponse | AsyncIterator[ChatCompletionStreamResponse]:
        """创建 Anthropic 格式对话完成请求.

        Args:
            model: 模型名称（Anthropic 格式）
            messages: 对话消息列表
            stream: 是否流式返回
            max_tokens: 最大生成 token 数
            temperature: 随机性控制
            top_p: 核采样阈值
            top_k: Top-k 采样
            stop: 停止序列

        Returns:
            对话完成响应或流式响应迭代器
        """
        # Anthropic 格式与 OpenAI 格式使用相同端点，通过模型名区分
        return await self.chat_completions(
            model=model,
            messages=messages,
            stream=stream,
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p,
            top_k=top_k,
            stop=stop,
        )

    async def rerank(
        self,
        model: str,
        query: str,
        documents: list[str],
        top_n: int | None = None,
        return_documents: bool | None = None,
        max_chunks_per_doc: int | None = None,
        overlap_tokens: int | None = None,
        instruction: str | None = None,
    ) -> RerankResponse:
        """创建重排序请求.

        Args:
            model: 模型名称，如 "BAAI/bge-reranker-v2-m3"
            query: 搜索查询文本
            documents: 待重排序的文档列表
            top_n: 返回最相关文档的数量
            return_documents: 是否返回原始文档文本
            max_chunks_per_doc: 单文档最大分块数
            overlap_tokens: 相邻分块重叠 token 数
            instruction: 重排序指令（仅特定 Qwen 模型支持）

        Returns:
            重排序响应，包含相关性分数和文档索引
        """
        payload: dict[str, Any] = {
            "model": model,
            "query": query,
            "documents": documents,
        }

        if top_n is not None:
            payload["top_n"] = top_n
        if return_documents is not None:
            payload["return_documents"] = return_documents
        if max_chunks_per_doc is not None:
            payload["max_chunks_per_doc"] = max_chunks_per_doc
        if overlap_tokens is not None:
            payload["overlap_tokens"] = overlap_tokens
        if instruction is not None:
            payload["instruction"] = instruction

        response = await self._http.post("rerank", json=payload)
        return self._http.parse_json(response)
