"""使用示例 - 演示如何使用核心功能"""

from src.core.style_mapper import StyleMapper
from src.core.prompt_generator import PromptGenerator


def example_1_list_styles():
    """示例1：列出所有可用风格"""
    print("=" * 60)
    print("示例 1: 列出所有可用风格")
    print("=" * 60)

    mapper = StyleMapper()
    styles = mapper.list_available_styles()

    for name, description in styles:
        print(f"\n🎨 {name}")
        print(f"   {description}")


def example_2_generate_prompt():
    """示例2：生成单个提示词"""
    print("\n" + "=" * 60)
    print("示例 2: 生成单个提示词")
    print("=" * 60)

    generator = PromptGenerator()

    # 图标列表
    icon_list = ["主页", "购物车", "设置"]
    style_name = "3D黏土风"

    print(f"\n📝 输入:")
    print(f"   图标: {', '.join(icon_list)}")
    print(f"   风格: {style_name}")

    # 生成提示词
    success, prompt, used_style = generator.generate(
        icon_list=icon_list,
        style_name=style_name,
        aspect_ratio="16:9"
    )

    if success:
        print(f"\n✅ 生成成功！")
        print(f"   使用风格: {used_style}")
        print(f"\n📄 生成的提示词:")
        print("-" * 60)
        print(prompt)
        print("-" * 60)
    else:
        print(f"\n❌ 生成失败: {prompt}")


def example_3_preview_translation():
    """示例3：预览图标翻译"""
    print("\n" + "=" * 60)
    print("示例 3: 预览图标翻译")
    print("=" * 60)

    generator = PromptGenerator()

    icon_list = [
        "主页", "购物车", "设置", "个人中心", "搜索",
        "消息", "收藏", "分享", "下载", "删除"
    ]

    print(f"\n📋 图标翻译预览:")
    preview = generator.preview_translation(icon_list)
    print(preview)


def example_4_different_styles():
    """示例4：不同风格对比"""
    print("\n" + "=" * 60)
    print("示例 4: 不同风格对比")
    print("=" * 60)

    generator = PromptGenerator()
    icon_list = ["主页", "设置"]

    styles = ["3D黏土风", "霓虹赛博朋克", "极简毛玻璃"]

    for style_name in styles:
        success, prompt, _ = generator.generate(
            icon_list=icon_list,
            style_name=style_name
        )

        if success:
            print(f"\n🎨 风格: {style_name}")
            print("-" * 60)
            # 只显示关键部分
            lines = prompt.split('\n')
            for line in lines:
                if line.startswith('[') or line.startswith('--'):
                    print(line)
            print("-" * 60)


def main():
    """运行所有示例"""
    print("\n")
    print("🎨" * 30)
    print("UI 风格化图标生成系统 - 使用示例")
    print("🎨" * 30)

    example_1_list_styles()
    example_2_generate_prompt()
    example_3_preview_translation()
    example_4_different_styles()

    print("\n" + "=" * 60)
    print("✅ 所有示例运行完成！")
    print("=" * 60)
    print("\n💡 提示: 运行 'python3 run.py' 启动完整的 Web 应用")
    print()


if __name__ == "__main__":
    main()
