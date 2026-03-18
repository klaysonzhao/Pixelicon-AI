"""任务管理器"""
import asyncio
import time
from pathlib import Path
from typing import List, Optional, Callable
from dataclasses import dataclass

from loguru import logger

from src.api.client import NanoBananaClient
from src.api.models import TaskResult, TaskFailedError, TimeoutError as APITimeoutError


@dataclass
class GenerationTask:
    """生成任务"""
    icon_name: str
    prompt: str
    task_id: Optional[str] = None
    result: Optional[TaskResult] = None
    error: Optional[str] = None


class TaskManager:
    """任务管理器"""

    def __init__(
        self,
        client: NanoBananaClient,
        max_concurrent: int = 3,
        initial_interval: float = 3.0,
        max_interval: float = 15.0,
        backoff_factor: float = 1.5
    ):
        """
        初始化任务管理器

        Args:
            client: API 客户端
            max_concurrent: 最大并发任务数
            initial_interval: 初始轮询间隔(秒)
            max_interval: 最大轮询间隔(秒)
            backoff_factor: 退避因子
        """
        self.client = client
        self.max_concurrent = max_concurrent
        self.initial_interval = initial_interval
        self.max_interval = max_interval
        self.backoff_factor = backoff_factor

    async def submit_and_poll(
        self,
        prompt: str,
        max_wait: int = 300,
        aspect_ratio: str = "16:9",
        resolution: str = "1K",
        output_format: str = "png",
        progress_callback: Optional[Callable[[str, float], None]] = None
    ) -> TaskResult:
        """
        提交任务并轮询结果

        Args:
            prompt: 提示词
            max_wait: 最大等待时间(秒)
            aspect_ratio: 宽高比
            resolution: 分辨率
            output_format: 输出格式
            progress_callback: 进度回调函数(状态消息, 已等待时间)

        Returns:
            任务结果

        Raises:
            TaskFailedError: 任务失败
            APITimeoutError: 超时
        """
        # 创建任务
        task_id = await self.client.create_task(
            prompt=prompt,
            aspect_ratio=aspect_ratio,
            resolution=resolution,
            output_format=output_format
        )

        # 轮询任务状态
        start_time = time.time()
        interval = self.initial_interval

        while time.time() - start_time < max_wait:
            elapsed = time.time() - start_time

            # 查询任务
            result = await self.client.query_task(task_id)

            # 更新进度
            if progress_callback:
                if result.is_waiting:
                    progress_callback(f"等待中... ({elapsed:.0f}秒)", elapsed)
                elif result.is_success:
                    progress_callback("生成完成", elapsed)

            # 检查任务状态
            if result.is_success:
                logger.success(f"任务完成: task_id={task_id}, cost_time={result.costTime}ms")
                return result

            if result.is_failed:
                error_msg = result.failMsg or "未知错误"
                logger.error(f"任务失败: task_id={task_id}, error={error_msg}")
                raise TaskFailedError(f"任务失败: {error_msg}")

            # 等待后重试
            await asyncio.sleep(interval)
            interval = min(interval * self.backoff_factor, self.max_interval)

        raise APITimeoutError(f"任务超时 ({max_wait}秒)")

    async def batch_generate(
        self,
        tasks: List[GenerationTask],
        max_wait: int = 300,
        aspect_ratio: str = "16:9",
        resolution: str = "1K",
        output_format: str = "png",
        progress_callback: Optional[Callable[[int, int, str], None]] = None
    ) -> List[GenerationTask]:
        """
        批量生成图标

        Args:
            tasks: 任务列表
            max_wait: 每个任务的最大等待时间(秒)
            aspect_ratio: 宽高比
            resolution: 分辨率
            output_format: 输出格式
            progress_callback: 进度回调函数(已完成数, 总数, 当前任务名)

        Returns:
            更新后的任务列表
        """
        semaphore = asyncio.Semaphore(self.max_concurrent)
        completed = 0

        async def process_one(task: GenerationTask, index: int):
            nonlocal completed

            async with semaphore:
                try:
                    if progress_callback:
                        progress_callback(completed, len(tasks), task.icon_name)

                    # 提交并轮询
                    result = await self.submit_and_poll(
                        prompt=task.prompt,
                        max_wait=max_wait,
                        aspect_ratio=aspect_ratio,
                        resolution=resolution,
                        output_format=output_format
                    )

                    task.result = result
                    task.task_id = result.taskId

                except Exception as e:
                    logger.error(f"任务失败: icon={task.icon_name}, error={e}")
                    task.error = str(e)

                finally:
                    completed += 1
                    if progress_callback:
                        progress_callback(completed, len(tasks), task.icon_name)

        # 并发执行所有任务
        await asyncio.gather(
            *[process_one(task, i) for i, task in enumerate(tasks)],
            return_exceptions=True
        )

        return tasks

    async def download_results(
        self,
        tasks: List[GenerationTask],
        output_dir: Path,
        progress_callback: Optional[Callable[[int, int], None]] = None
    ) -> List[Path]:
        """
        下载生成结果

        Args:
            tasks: 任务列表
            output_dir: 输出目录
            progress_callback: 进度回调函数(已完成数, 总数)

        Returns:
            下载的文件路径列表
        """
        downloaded_files = []
        completed = 0

        for task in tasks:
            if not task.result or not task.result.is_success:
                continue

            urls = task.result.get_result_urls()
            if not urls:
                continue

            # 下载第一个结果
            url = urls[0]
            filename = f"{task.icon_name}_{task.task_id[:8]}.png"
            save_path = output_dir / filename

            try:
                downloaded = await self.client.download_image(url, save_path)
                downloaded_files.append(downloaded)
            except Exception as e:
                logger.error(f"下载失败: icon={task.icon_name}, error={e}")

            completed += 1
            if progress_callback:
                progress_callback(completed, len(tasks))

        return downloaded_files
