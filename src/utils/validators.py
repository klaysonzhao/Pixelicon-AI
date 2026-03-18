"""输入验证工具"""
import re
from typing import List


def validate_icon_list(icon_text: str) -> tuple[bool, str, List[str]]:
    """
    验证图标清单输入

    Args:
        icon_text: 用户输入的图标清单文本

    Returns:
        (是否有效, 错误信息, 图标列表)
    """
    if not icon_text or not icon_text.strip():
        return False, "图标清单不能为空", []

    # 分割图标
    icons = [icon.strip() for icon in re.split(r'[,，、]', icon_text) if icon.strip()]

    if len(icons) < 1:
        return False, "至少需要输入 1 个图标", []

    if len(icons) > 10:
        return False, "图标数量不能超过 10 个", []

    return True, "", icons


def validate_api_key(api_key: str) -> tuple[bool, str]:
    """
    验证 API Key 格式

    Args:
        api_key: API Key

    Returns:
        (是否有效, 错误信息)
    """
    if not api_key or not api_key.strip():
        return False, "API Key 不能为空"

    # 基本长度检查
    if len(api_key.strip()) < 10:
        return False, "API Key 格式无效（长度过短）"

    return True, ""
