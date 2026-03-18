"""风格映射系统"""
from pathlib import Path
from typing import Optional, Dict, List
import yaml
from dataclasses import dataclass
from loguru import logger


@dataclass
class StyleComponents:
    """风格组件"""
    name: str
    medium: str
    material: str
    lighting: str
    background: str
    description: str


class StyleMapper:
    """风格映射器"""

    def __init__(self, config_path: Optional[Path] = None):
        """
        初始化风格映射器

        Args:
            config_path: 配置文件路径
        """
        if config_path is None:
            config_path = Path(__file__).parent.parent.parent / "config" / "styles.yaml"

        self.config_path = config_path
        self.styles: Dict[str, Dict[str, str]] = {}
        self._load_styles()

    def _load_styles(self):
        """加载风格配置"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
                self.styles = data.get('styles', {})
            logger.info(f"加载了 {len(self.styles)} 个风格配置")
        except Exception as e:
            logger.error(f"加载风格配置失败: {e}")
            self.styles = {}

    def get_style_components(self, style_name: str) -> Optional[StyleComponents]:
        """
        获取风格组件

        Args:
            style_name: 风格名称

        Returns:
            风格组件对象，如果不存在则返回 None
        """
        style_data = self.styles.get(style_name)
        if not style_data:
            # 尝试模糊匹配
            matched = self.fuzzy_match(style_name)
            if matched:
                style_data = self.styles[matched]
                style_name = matched
            else:
                return None

        return StyleComponents(
            name=style_name,
            medium=style_data.get('medium', ''),
            material=style_data.get('material', ''),
            lighting=style_data.get('lighting', ''),
            background=style_data.get('background', 'solid white background'),
            description=style_data.get('description', '')
        )

    def fuzzy_match(self, user_input: str) -> Optional[str]:
        """
        模糊匹配风格名称

        Args:
            user_input: 用户输入

        Returns:
            匹配的风格名称，如果没有匹配则返回 None
        """
        user_input = user_input.strip().lower()

        # 完全匹配
        for style_name in self.styles.keys():
            if style_name.lower() == user_input:
                return style_name

        # 包含匹配
        for style_name in self.styles.keys():
            if user_input in style_name.lower() or style_name.lower() in user_input:
                return style_name

        return None

    def list_available_styles(self) -> List[tuple[str, str]]:
        """
        列出所有可用风格

        Returns:
            (风格名称, 描述) 的列表
        """
        return [
            (name, data.get('description', ''))
            for name, data in self.styles.items()
        ]

    def get_style_names(self) -> List[str]:
        """获取所有风格名称"""
        return list(self.styles.keys())
