"""配置管理模块"""
import os
from pathlib import Path
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """应用配置"""
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        case_sensitive=False
    )

    # API 配置
    nano_banana_api_key: str = Field(default="", description="Nano Banana API Key")
    nano_banana_base_url: str = Field(
        default="https://api.kie.ai/api/v1",
        description="API Base URL"
    )

    # 日志配置
    log_level: str = Field(default="INFO", description="日志级别")

    # 任务配置
    max_concurrent_tasks: int = Field(default=3, description="最大并发任务数")
    default_timeout: int = Field(default=300, description="默认超时时间(秒)")
    poll_interval: int = Field(default=3, description="轮询间隔(秒)")

    # 输出配置
    output_dir: str = Field(default="./data/generated", description="输出目录")

    @property
    def output_path(self) -> Path:
        """获取输出路径对象"""
        path = Path(self.output_dir)
        path.mkdir(parents=True, exist_ok=True)
        return path


# 全局配置实例
settings = Settings()
