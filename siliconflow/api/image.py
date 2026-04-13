"""图像系列 API.

包含：图片生成
"""

from typing import Any

from .._http import HTTPClient
from .._types import ImageGenerationResponse


class ImageAPI:
    """图像系列 API.

    包含图像生成相关接口.
    """

    def __init__(self, http: HTTPClient):
        """初始化图像 API 客户端.

        Args:
            http: HTTP 客户端实例
        """
        self._http = http

    async def generations(
        self,
        model: str,
        prompt: str,
        negative_prompt: str | None = None,
        image_size: str | None = None,
        batch_size: int | None = None,
        seed: int | None = None,
        num_inference_steps: int | None = None,
        guidance_scale: float | None = None,
        cfg: float | None = None,
        image: str | None = None,
        image2: str | None = None,
        image3: str | None = None,
    ) -> ImageGenerationResponse:
        """创建图片生成请求.

        Args:
            model: 模型名称，如 "Kwai-Kolors/Kolors" 或 "Qwen/Qwen-Image-Edit-2509"
            prompt: 生成图片的文本描述
            negative_prompt: 负面提示词
            image_size: 分辨率格式 "widthxheight"，Qwen-Image-Edit 不支持
            batch_size: 输出图片数量 (1-4)，默认 1，仅 Kolors 适用
            seed: 随机种子 (0-9999999999)
            num_inference_steps: 推理步数 (1-100)，默认 20
            guidance_scale: 提示匹配度 (0-20)，默认 7.5，仅 Kolors 适用
            cfg: CFG 值 (0.1-20)，仅 Qwen-Image 适用
            image: 参考图片 URL 或 base64
            image2: 参考图片 2，仅 Qwen-Image-Edit-2509
            image3: 参考图片 3，仅 Qwen-Image-Edit-2509

        Returns:
            图像生成响应，包含图片 URL（有效期1小时）

        Note:
            生成的图片 URL 有效期为1小时，请及时下载保存
        """
        payload: dict[str, Any] = {
            "model": model,
            "prompt": prompt,
        }

        if negative_prompt is not None:
            payload["negative_prompt"] = negative_prompt
        if image_size is not None:
            payload["image_size"] = image_size
        if batch_size is not None:
            payload["batch_size"] = batch_size
        if seed is not None:
            payload["seed"] = seed
        if num_inference_steps is not None:
            payload["num_inference_steps"] = num_inference_steps
        if guidance_scale is not None:
            payload["guidance_scale"] = guidance_scale
        if cfg is not None:
            payload["cfg"] = cfg
        if image is not None:
            payload["image"] = image
        if image2 is not None:
            payload["image2"] = image2
        if image3 is not None:
            payload["image3"] = image3

        response = await self._http.post("images/generations", json=payload)
        return self._http.parse_json(response)
