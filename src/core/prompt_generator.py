"""提示词生成器"""
from pathlib import Path
from typing import List, Optional, Dict
import yaml
from jinja2 import Template
from loguru import logger

from src.core.style_mapper import StyleMapper, StyleComponents


class PromptGenerator:
    """提示词生成器"""

    # 提示词模板（基于 prompot.md）
    TEMPLATE = """A professional UI icon set featuring {{icons_en}}.

[Style & Medium]
{{style.medium}}

[Material & Texture]
{{style.material}}

[Lighting, Rendering & Color]
{{style.lighting}}

[UI Constraints]
Professional UI design asset, {{style.background}}, isolated objects, front-facing, perfectly spaced grid layout, vector-like clean edges, high resolution, 8k, dribbble trending.
--v 6.0 --ar {{aspect_ratio}} --stylize 250"""

    def __init__(
        self,
        style_mapper: Optional[StyleMapper] = None,
        icon_translations_path: Optional[Path] = None
    ):
        """
        初始化提示词生成器

        Args:
            style_mapper: 风格映射器
            icon_translations_path: 图标翻译配置路径
        """
        self.style_mapper = style_mapper or StyleMapper()

        if icon_translations_path is None:
            icon_translations_path = Path(__file__).parent.parent.parent / "config" / "icon_translations.yaml"

        self.icon_translations: Dict[str, str] = {}
        self._load_icon_translations(icon_translations_path)

        self.template = Template(self.TEMPLATE)

    def _load_icon_translations(self, path: Path):
        """加载图标翻译配置"""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                # YAML文件中是键值对格式
                self.icon_translations = yaml.safe_load(f) or {}
            logger.info(f"加载了 {len(self.icon_translations)} 个图标翻译")
        except Exception as e:
            logger.error(f"加载图标翻译失败: {e}")
            self.icon_translations = {}

    def translate_icon(self, icon_name: str) -> str:
        """
        翻译图标名称

        Args:
            icon_name: 中文图标名称

        Returns:
            英文翻译
        """
        # 去除空格
        icon_name = icon_name.strip()

        # 从翻译表查找
        translation = self.icon_translations.get(icon_name)
        if translation:
            return translation

        # 如果没有找到，使用原名称（可能本身就是英文）
        logger.warning(f"未找到图标翻译: {icon_name}，使用原名称")
        return f"a {icon_name}"

    def translate_icons(self, icon_list: List[str]) -> str:
        """
        翻译图标列表

        Args:
            icon_list: 中文图标名称列表

        Returns:
            英文翻译字符串（逗号分隔）
        """
        translations = [self.translate_icon(icon) for icon in icon_list]
        return ", ".join(translations)

    def generate(
        self,
        icon_list: List[str],
        style_name: str,
        aspect_ratio: str = "16:9"
    ) -> tuple[bool, str, Optional[str]]:
        """
        生成提示词

        Args:
            icon_list: 图标列表
            style_name: 风格名称
            aspect_ratio: 宽高比

        Returns:
            (是否成功, 错误信息或提示词, 使用的风格名称)
        """
        # 获取风格组件
        style = self.style_mapper.get_style_components(style_name)
        if not style:
            available_styles = ", ".join(self.style_mapper.get_style_names())
            return False, f"未找到风格: {style_name}。可用风格: {available_styles}", None

        # 翻译图标
        icons_en = self.translate_icons(icon_list)

        # 生成提示词
        try:
            prompt = self.template.render(
                icons_en=icons_en,
                style=style,
                aspect_ratio=aspect_ratio
            )
            logger.success(f"成功生成提示词: style={style.name}, icons={len(icon_list)}")
            return True, prompt.strip(), style.name

        except Exception as e:
            logger.error(f"生成提示词失败: {e}")
            return False, f"生成提示词失败: {str(e)}", None

    def preview_translation(self, icon_list: List[str]) -> str:
        """
        预览图标翻译

        Args:
            icon_list: 图标列表

        Returns:
            翻译预览文本
        """
        lines = []
        for icon in icon_list:
            translation = self.translate_icon(icon)
            lines.append(f"  • {icon} → {translation}")
        return "\n".join(lines)
