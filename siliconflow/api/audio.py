"""语音系列 API.

包含：语音转文本、文本转语音、参考音频管理
"""

from typing import Any, BinaryIO

from .._http import HTTPClient
from .._types import (
    TranscriptionResponse,
    VoiceListResponse,
    VoiceUploadResponse,
)


class AudioAPI:
    """语音系列 API.

    包含语音转文本、文本转语音、参考音频管理相关接口.
    """

    def __init__(self, http: HTTPClient):
        """初始化语音 API 客户端.

        Args:
            http: HTTP 客户端实例
        """
        self._http = http

    async def transcriptions(
        self,
        file: BinaryIO,
        model: str,
    ) -> TranscriptionResponse:
        """语音转文本.

        Args:
            file: 音频文件对象，时长不超过1小时，大小不超过50MB
            model: 模型名称，如 "FunAudioLLM/SenseVoiceSmall" 或 "TeleAI/TeleSpeechASR"

        Returns:
            转录文本响应
        """
        files = {
            "file": file,
        }
        data = {
            "model": model,
        }

        response = await self._http.post_form(
            "audio/transcriptions",
            data=data,
            files=files,
        )
        return self._http.parse_json(response)

    async def speech(
        self,
        model: str,
        input: str,
        voice: str | None = None,
        references: list[dict[str, str]] | None = None,
        response_format: str = "mp3",
        sample_rate: int | None = None,
        stream: bool = True,
        speed: float = 1.0,
        gain: float = 0.0,
        max_tokens: int | None = None,
    ) -> bytes:
        """文本转语音.

        Args:
            model: 模型名称，如 "fnlp/MOSS-TTSD-v0.5" 或 "FunAudioLLM/CosyVoice2-0.5B"
            input: 输入文本
                - MOSS: 带说话人标签的对话文本 [S1] [S2]
                - CosyVoice: 带自然语言指令的文本，以 <|endofprompt|> 结尾
            voice: 预设声音，可选: alex, anna, bella, benjamin, charles, claire, david, diana
            references: 声音克隆参考，与 voice 互斥，格式 [{"audio": "...", "text": "..."}]
            response_format: 输出格式，mp3/opus/wav/pcm，默认 mp3
            sample_rate: 采样率
            stream: 是否流式返回，默认 True
            speed: 语速 (0.25-4.0)，默认 1.0
            gain: 音量增益 (-10 到 10)，默认 0
            max_tokens: 最大 token 数，默认 2048

        Returns:
            音频二进制数据
        """
        payload: dict[str, Any] = {
            "model": model,
            "input": input,
            "response_format": response_format,
            "stream": stream,
            "speed": speed,
            "gain": gain,
        }

        if voice is not None:
            payload["voice"] = voice
        if references is not None:
            payload["references"] = references
        if sample_rate is not None:
            payload["sample_rate"] = sample_rate
        if max_tokens is not None:
            payload["max_tokens"] = max_tokens

        response = await self._http.post("audio/speech", json=payload)
        return response.content

    async def voice_list(self) -> VoiceListResponse:
        """获取参考音频列表.

        Returns:
            用户预定义音色风格列表
        """
        response = await self._http.get("audio/voice/list")
        return self._http.parse_json(response)

    async def voice_upload(
        self,
        file: BinaryIO,
        model: str,
        custom_name: str,
        text: str,
    ) -> VoiceUploadResponse:
        """上传参考音频.

        Args:
            file: 音频文件
            model: 模型名称
            custom_name: 用户自定义音色名称
            text: 音频对应的文本内容

        Returns:
            上传响应，包含生成的 URI
        """
        files = {
            "file": file,
        }
        data = {
            "model": model,
            "customName": custom_name,
            "text": text,
        }

        response = await self._http.post_form(
            "audio/voice/upload",
            data=data,
            files=files,
        )
        return self._http.parse_json(response)

    async def voice_delete(self, uri: str) -> None:
        """删除参考音频.

        Args:
            uri: 音频 URI，格式如 speech:your-voice-name:xxx:xxx
        """
        await self._http.delete("audio/voice/delete", headers={"X-Voice-Uri": uri})
