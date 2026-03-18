"""Nano Banana API 客户端"""
import asyncio
from pathlib import Path
from typing import Optional

import httpx
from loguru import logger
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type
)

from src.api.models import (
    CreateTaskRequest,
    CreateTaskInput,
    CreateTaskResponse,
    QueryTaskResponse,
    TaskResult,
    APIError,
    AuthenticationError,
    RateLimitError,
    InsufficientBalanceError
)


class NanoBananaClient:
    """Nano Banana API 客户端"""

    def __init__(self, api_key: str, base_url: str = "https://api.kie.ai/api/v1"):
        """
        初始化客户端

        Args:
            api_key: API Key
            base_url: API Base URL
        """
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.client = httpx.AsyncClient(
            timeout=30.0,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
        )

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def close(self):
        """关闭客户端"""
        await self.client.aclose()

    def _handle_error(self, status_code: int, response_text: str):
        """处理API错误"""
        error_map = {
            401: AuthenticationError("认证失败，请检查 API Key 是否正确"),
            402: InsufficientBalanceError("账户余额不足，请充值后重试"),
            429: RateLimitError("请求过于频繁，请稍后重试"),
        }

        if status_code in error_map:
            raise error_map[status_code]

        raise APIError(f"API 请求失败 (HTTP {status_code}): {response_text}")

    @retry(
        retry=retry_if_exception_type((httpx.ConnectError, httpx.TimeoutException)),
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    async def create_task(
        self,
        prompt: str,
        aspect_ratio: str = "16:9",
        resolution: str = "1K",
        output_format: str = "png",
        image_input: Optional[list] = None
    ) -> str:
        """
        创建生成任务

        Args:
            prompt: 提示词
            aspect_ratio: 宽高比
            resolution: 分辨率
            output_format: 输出格式
            image_input: 输入图像URL列表

        Returns:
            任务ID
        """
        url = f"{self.base_url}/jobs/createTask"

        request_data = CreateTaskRequest(
            model="nano-banana-2",
            input=CreateTaskInput(
                prompt=prompt,
                aspect_ratio=aspect_ratio,
                resolution=resolution,
                output_format=output_format,
                image_input=image_input
            )
        )

        logger.info(f"创建任务: prompt_length={len(prompt)}, resolution={resolution}")

        try:
            response = await self.client.post(
                url,
                json=request_data.model_dump(exclude_none=True)
            )

            if response.status_code != 200:
                self._handle_error(response.status_code, response.text)

            result = CreateTaskResponse(**response.json())

            if result.code != 200:
                raise APIError(f"创建任务失败: {result.msg}")

            task_id = result.task_id
            logger.success(f"任务创建成功: task_id={task_id}")
            return task_id

        except httpx.HTTPError as e:
            logger.error(f"HTTP 请求失败: {e}")
            raise APIError(f"网络请求失败: {str(e)}")

    @retry(
        retry=retry_if_exception_type((httpx.ConnectError, httpx.TimeoutException)),
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    async def query_task(self, task_id: str) -> TaskResult:
        """
        查询任务状态

        Args:
            task_id: 任务ID

        Returns:
            任务结果
        """
        url = f"{self.base_url}/jobs/recordInfo"
        params = {"taskId": task_id}

        try:
            response = await self.client.get(url, params=params)

            if response.status_code != 200:
                self._handle_error(response.status_code, response.text)

            result = QueryTaskResponse(**response.json())

            if result.code != 200:
                raise APIError(f"查询任务失败: {result.msg}")

            return result.data

        except httpx.HTTPError as e:
            logger.error(f"HTTP 请求失败: {e}")
            raise APIError(f"网络请求失败: {str(e)}")

    async def download_image(self, url: str, save_path: Path) -> Path:
        """
        下载图像

        Args:
            url: 图像URL
            save_path: 保存路径

        Returns:
            保存的文件路径
        """
        logger.info(f"下载图像: {url}")

        try:
            # 确保目录存在
            save_path.parent.mkdir(parents=True, exist_ok=True)

            # 下载图像
            response = await self.client.get(url)
            response.raise_for_status()

            # 保存文件
            save_path.write_bytes(response.content)
            logger.success(f"图像下载成功: {save_path}")

            return save_path

        except httpx.HTTPError as e:
            logger.error(f"下载图像失败: {e}")
            raise APIError(f"下载图像失败: {str(e)}")
