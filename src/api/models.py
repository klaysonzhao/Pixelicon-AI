"""API 数据模型"""
from typing import Optional, List
from pydantic import BaseModel, Field


class CreateTaskInput(BaseModel):
    """创建任务的输入参数"""
    prompt: str = Field(..., description="图像描述提示词", max_length=20000)
    image_input: Optional[List[str]] = Field(default=None, description="输入图像URL列表")
    aspect_ratio: str = Field(default="16:9", description="宽高比")
    resolution: str = Field(default="1K", description="分辨率")
    output_format: str = Field(default="png", description="输出格式")


class CreateTaskRequest(BaseModel):
    """创建任务请求"""
    model: str = Field(default="nano-banana-2", description="模型名称")
    input: CreateTaskInput = Field(..., description="输入参数")
    callBackUrl: Optional[str] = Field(default=None, description="回调URL")


class CreateTaskResponse(BaseModel):
    """创建任务响应"""
    code: int
    msg: str
    data: dict

    @property
    def task_id(self) -> str:
        """获取任务ID"""
        return self.data.get("taskId", "")


class TaskResult(BaseModel):
    """任务结果"""
    taskId: str = Field(..., description="任务ID")
    model: str = Field(..., description="模型名称")
    state: str = Field(..., description="任务状态: waiting, success, fail")
    param: str = Field(..., description="任务参数JSON字符串")
    resultJson: Optional[str] = Field(default=None, description="结果JSON字符串")
    failCode: Optional[str] = Field(default=None, description="失败代码")
    failMsg: Optional[str] = Field(default=None, description="失败消息")
    costTime: Optional[int] = Field(default=None, description="耗时(毫秒)")
    completeTime: Optional[int] = Field(default=None, description="完成时间戳")
    createTime: int = Field(..., description="创建时间戳")

    @property
    def is_success(self) -> bool:
        """是否成功"""
        return self.state == "success"

    @property
    def is_failed(self) -> bool:
        """是否失败"""
        return self.state == "fail"

    @property
    def is_waiting(self) -> bool:
        """是否等待中"""
        return self.state == "waiting"

    def get_result_urls(self) -> List[str]:
        """获取结果URL列表"""
        if not self.resultJson:
            return []
        import json
        try:
            result_data = json.loads(self.resultJson)
            return result_data.get("resultUrls", [])
        except Exception:
            return []


class QueryTaskResponse(BaseModel):
    """查询任务响应"""
    code: int
    msg: str
    data: TaskResult


# 自定义异常
class APIError(Exception):
    """API错误基类"""
    pass


class AuthenticationError(APIError):
    """认证错误"""
    pass


class RateLimitError(APIError):
    """速率限制错误"""
    pass


class InsufficientBalanceError(APIError):
    """余额不足错误"""
    pass


class TaskFailedError(APIError):
    """任务失败错误"""
    pass


class TimeoutError(APIError):
    """超时错误"""
    pass
