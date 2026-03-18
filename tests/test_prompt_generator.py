"""测试提示词生成器"""
import pytest
from src.core.style_mapper import StyleMapper
from src.core.prompt_generator import PromptGenerator


def test_style_mapper():
    """测试风格映射器"""
    mapper = StyleMapper()

    # 测试获取风格
    style = mapper.get_style_components("3D黏土风")
    assert style is not None
    assert "3D" in style.medium
    assert style.background == "solid white background"

    # 测试列出所有风格
    styles = mapper.list_available_styles()
    assert len(styles) > 0


def test_prompt_generator():
    """测试提示词生成器"""
    generator = PromptGenerator()

    # 测试图标翻译
    translation = generator.translate_icon("主页")
    assert translation == "a house"

    # 测试批量翻译
    translations = generator.translate_icons(["主页", "购物车", "设置"])
    assert "house" in translations
    assert "shopping cart" in translations
    assert "gear" in translations

    # 测试生成提示词
    success, prompt, style_name = generator.generate(
        icon_list=["主页", "购物车"],
        style_name="3D黏土风",
        aspect_ratio="16:9"
    )
    assert success is True
    assert "house" in prompt
    assert "shopping cart" in prompt
    assert "3D" in prompt
    assert "--v 6.0" in prompt
    assert "--ar 16:9" in prompt


def test_prompt_generator_invalid_style():
    """测试无效风格"""
    generator = PromptGenerator()

    success, error_msg, style_name = generator.generate(
        icon_list=["主页"],
        style_name="不存在的风格"
    )
    assert success is False
    assert "未找到风格" in error_msg


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
