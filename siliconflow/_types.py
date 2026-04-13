"""SiliconFlow API 类型定义.

使用 TypedDict 定义所有请求和响应类型.
"""

from typing import Any, Literal, NotRequired, TypedDict


# ============================================================================
# 通用类型
# ============================================================================

class Usage(TypedDict):
    """Token 使用情况."""

    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    prompt_cache_hit_tokens: NotRequired[int]
    prompt_cache_miss_tokens: NotRequired[int]
    completion_tokens_details: NotRequired[dict[str, Any]]
    prompt_tokens_details: NotRequired[dict[str, Any]]


# ============================================================================
# 文本系列 - Embeddings
# ============================================================================

class EmbeddingData(TypedDict):
    """单个嵌入结果."""

    object: Literal["embedding"]
    embedding: list[float]
    index: int


class EmbeddingResponse(TypedDict):
    """嵌入响应."""

    object: Literal["list"]
    model: str
    data: list[EmbeddingData]
    usage: Usage


# ============================================================================
# 文本系列 - Chat Completions
# ============================================================================

class Message(TypedDict):
    """对话消息."""

    role: Literal["system", "user", "assistant", "tool"]
    content: str | list[dict[str, Any]]
    name: NotRequired[str]
    tool_calls: NotRequired[list[dict[str, Any]]]


class Choice(TypedDict):
    """生成选项."""

    index: int
    message: Message
    finish_reason: Literal["stop", "eos", "length", "tool_calls"]
    logprobs: NotRequired[dict[str, Any]]


class ChoiceDelta(TypedDict):
    """流式响应的 delta."""

    role: NotRequired[str]
    content: NotRequired[str]
    reasoning_content: NotRequired[str]
    tool_calls: NotRequired[list[dict[str, Any]]]


class StreamChoice(TypedDict):
    """流式生成选项."""

    index: int
    delta: ChoiceDelta
    finish_reason: NotRequired[str]


class ChatCompletionResponse(TypedDict):
    """对话完成响应."""

    id: str
    object: Literal["chat.completion"]
    created: int
    model: str
    choices: list[Choice]
    usage: Usage
    system_fingerprint: NotRequired[str]


class ChatCompletionStreamResponse(TypedDict):
    """流式对话完成响应."""

    id: str
    object: Literal["chat.completion.chunk"]
    created: int
    model: str
    choices: list[StreamChoice]
    system_fingerprint: NotRequired[str]


# ============================================================================
# 文本系列 - Rerank
# ============================================================================

class RerankDocument(TypedDict):
    """重排序文档."""

    text: str


class RerankResult(TypedDict):
    """重排序结果."""

    index: int
    relevance_score: float
    document: NotRequired[RerankDocument]


class RerankMeta(TypedDict):
    """重排序元数据."""

    tokens: dict[str, int]


class RerankResponse(TypedDict):
    """重排序响应."""

    id: str
    results: list[RerankResult]
    meta: list[RerankMeta]


# ============================================================================
# 图像系列
# ============================================================================

class ImageData(TypedDict):
    """生成图像数据."""

    url: str


class ImageTimings(TypedDict):
    """图像生成时间统计."""

    inference: float


class ImageGenerationResponse(TypedDict):
    """图像生成响应."""

    images: list[ImageData]
    timings: ImageTimings
    seed: int


# ============================================================================
# 语音系列 - Transcriptions
# ============================================================================

class TranscriptionResponse(TypedDict):
    """语音转文本响应."""

    text: str


# ============================================================================
# 语音系列 - Voice
# ============================================================================

class VoiceInfo(TypedDict):
    """参考音频信息."""

    model: str
    customName: str
    text: str
    uri: str


class VoiceListResponse(TypedDict):
    """参考音频列表响应."""

    results: list[VoiceInfo]


class VoiceUploadResponse(TypedDict):
    """上传参考音频响应."""

    uri: str


# ============================================================================
# 视频系列
# ============================================================================

class VideoStatus(TypedDict):
    """视频状态."""

    status: Literal["pending", "processing", "completed", "failed"]
    url: NotRequired[str]
    error: NotRequired[str]


class VideoGenerationResponse(TypedDict):
    """视频生成响应."""

    id: str
    status: str
    url: NotRequired[str]


# ============================================================================
# 批量处理 - Batch
# ============================================================================

class Batch(TypedDict):
    """Batch 任务信息."""

    id: str
    object: Literal["batch"]
    endpoint: str
    errors: NotRequired[dict[str, Any]]
    input_file_id: str
    completion_window: str
    status: Literal[
        "validating",
        "failed",
        "in_progress",
        "finalizing",
        "completed",
        "expired",
        "cancelling",
        "cancelled",
    ]
    output_file_id: NotRequired[str]
    error_file_id: NotRequired[str]
    created_at: int
    in_progress_at: NotRequired[int]
    expires_at: NotRequired[int]
    finalizing_at: NotRequired[int]
    completed_at: NotRequired[int]
    failed_at: NotRequired[int]
    expired_at: NotRequired[int]
    cancelling_at: NotRequired[int]
    cancelled_at: NotRequired[int]
    request_counts: NotRequired[dict[str, int]]
    metadata: NotRequired[dict[str, Any]]


class BatchListResponse(TypedDict):
    """Batch 列表响应."""

    object: Literal["list"]
    data: list[Batch]
    first_id: NotRequired[str]
    last_id: NotRequired[str]
    has_more: bool


# ============================================================================
# 批量处理 - Files
# ============================================================================

class FileInfo(TypedDict):
    """文件信息."""

    id: str
    object: Literal["file"]
    bytes: int
    created_at: int
    filename: str
    purpose: str
    status: Literal["uploaded", "processed", "error"]
    status_details: NotRequired[str]


class FileListResponse(TypedDict):
    """文件列表响应."""

    object: Literal["list"]
    data: list[FileInfo]


class FileUploadResponse(FileInfo):
    """文件上传响应."""

    pass


# ============================================================================
# 平台系列 - Models
# ============================================================================

class ModelInfo(TypedDict):
    """模型信息."""

    id: str
    object: Literal["model"]
    created: int
    owned_by: str
    permission: NotRequired[list[dict[str, Any]]]


class ModelListResponse(TypedDict):
    """模型列表响应."""

    object: Literal["list"]
    data: list[ModelInfo]
