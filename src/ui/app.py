"""UI 风格化图标生成系统 - Streamlit 应用"""
import asyncio
from pathlib import Path
from datetime import datetime
import zipfile
import io

import streamlit as st
from PIL import Image

from src.api.client import NanoBananaClient
from src.api.models import (
    APIError,
    AuthenticationError,
    RateLimitError,
    InsufficientBalanceError,
    TaskFailedError
)
from src.core.style_mapper import StyleMapper
from src.core.prompt_generator import PromptGenerator
from src.core.task_manager import TaskManager, GenerationTask
from src.utils.config import settings
from src.utils.validators import validate_icon_list, validate_api_key


# 页面配置
st.set_page_config(
    page_title="UI 图标生成系统",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义CSS - 现代极简风格
st.markdown("""
<style>
    /* 全局样式 */
    .main {
        background-color: #fafafa;
    }

    /* 主标题 */
    .main-header {
        text-align: center;
        padding: 2rem 0 1rem 0;
        color: #1a1a1a;
        font-weight: 700;
        letter-spacing: -0.5px;
    }

    .main-subtitle {
        text-align: center;
        color: #666;
        font-size: 1rem;
        font-weight: 400;
        margin-bottom: 2rem;
    }

    /* 步骤标题 - 极简风格 */
    .step-header {
        background: white;
        color: #1a1a1a;
        padding: 1rem 1.5rem;
        border-radius: 12px;
        margin: 1.5rem 0 1rem 0;
        border: 1px solid #e5e5e5;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
        font-weight: 600;
        font-size: 1.05rem;
    }

    /* API设置卡片 - 白色卡片风格 */
    .api-settings-card {
        background: white;
        border-radius: 12px;
        padding: 2rem;
        margin-bottom: 2rem;
        border: 1px solid #e5e5e5;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
    }

    .api-settings-card h3 {
        margin: 0 0 1.2rem 0;
        color: #1a1a1a;
        font-size: 1.1rem;
        font-weight: 600;
        letter-spacing: -0.3px;
    }

    .api-status {
        margin-top: 1rem;
        font-size: 0.9rem;
        padding: 0.6rem 1rem;
        border-radius: 8px;
        display: inline-block;
        font-weight: 500;
    }

    .api-status-success {
        background: #f0fdf4;
        border: 1px solid #bbf7d0;
        color: #15803d;
    }

    .api-status-warning {
        background: #fef3c7;
        border: 1px solid #fde68a;
        color: #92400e;
    }

    /* 输入框样式 - 简洁边框 */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        border: 1px solid #d1d5db !important;
        border-radius: 8px !important;
        padding: 0.75rem 1rem !important;
        font-size: 0.95rem !important;
        background: white !important;
        transition: all 0.2s ease !important;
    }

    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #1a1a1a !important;
        box-shadow: 0 0 0 3px rgba(0, 0, 0, 0.05) !important;
    }

    .stTextInput > div > div > input::placeholder,
    .stTextArea > div > div > textarea::placeholder {
        color: #9ca3af !important;
    }

    /* 下拉框样式 */
    .stSelectbox > div > div {
        border: 1px solid #d1d5db !important;
        border-radius: 8px !important;
        background: white !important;
    }

    /* 按钮样式 - 黑色主按钮 */
    .stButton > button {
        background: #1a1a1a !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.7rem 1.5rem !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        transition: all 0.2s ease !important;
        letter-spacing: 0.3px !important;
    }

    .stButton > button:hover {
        background: #000 !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15) !important;
        transform: translateY(-1px);
    }

    /* 次要按钮 */
    .stButton > button[kind="secondary"] {
        background: white !important;
        color: #1a1a1a !important;
        border: 1px solid #d1d5db !important;
    }

    .stButton > button[kind="secondary"]:hover {
        background: #f9fafb !important;
        border-color: #1a1a1a !important;
    }

    /* 成功/错误消息 */
    .stSuccess {
        background: #f0fdf4 !important;
        border: 1px solid #bbf7d0 !important;
        color: #15803d !important;
        border-radius: 8px !important;
        padding: 0.75rem 1rem !important;
    }

    .stError {
        background: #fef2f2 !important;
        border: 1px solid #fecaca !important;
        color: #991b1b !important;
        border-radius: 8px !important;
        padding: 0.75rem 1rem !important;
    }

    .stWarning {
        background: #fef3c7 !important;
        border: 1px solid #fde68a !important;
        color: #92400e !important;
        border-radius: 8px !important;
        padding: 0.75rem 1rem !important;
    }

    /* 图标预览 */
    .icon-preview {
        border: 1px solid #e5e5e5;
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem;
        background: white;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
        transition: all 0.2s ease;
    }

    .icon-preview:hover {
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
        transform: translateY(-2px);
    }

    /* 代码块样式 */
    .stCodeBlock {
        border: 1px solid #e5e5e5 !important;
        border-radius: 8px !important;
        background: #fafafa !important;
    }

    /* 进度条 */
    .stProgress > div > div {
        background-color: #1a1a1a !important;
        border-radius: 4px !important;
    }

    /* 展开器 */
    .streamlit-expanderHeader {
        background: white !important;
        border: 1px solid #e5e5e5 !important;
        border-radius: 8px !important;
        font-weight: 500 !important;
    }

    /* 隐藏默认的Streamlit标记 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* 卡片容器 */
    .card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        border: 1px solid #e5e5e5;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
        margin-bottom: 1rem;
    }

    /* 分隔线 */
    hr {
        border: none;
        border-top: 1px solid #e5e5e5;
        margin: 2rem 0;
    }
</style>
""", unsafe_allow_html=True)


def init_session_state():
    """初始化会话状态"""
    if 'api_key' not in st.session_state:
        st.session_state.api_key = settings.nano_banana_api_key or ""
    if 'saved_api_key' not in st.session_state:
        st.session_state.saved_api_key = ""
    if 'generated_tasks' not in st.session_state:
        st.session_state.generated_tasks = []
    if 'current_prompt' not in st.session_state:
        st.session_state.current_prompt = ""


def render_api_settings_card():
    """渲染API设置卡片 - 极简白色风格"""
    st.markdown('<div class="api-settings-card">', unsafe_allow_html=True)

    st.markdown("### 🔑 API 配置")

    col1, col2 = st.columns([4, 1])

    with col1:
        # API Key输入框
        api_key_input = st.text_input(
            "Nano Banana API Key",
            value=st.session_state.get('saved_api_key', ''),
            type="password",
            placeholder="请输入 API Key（在 https://kie.ai/api-key 获取）",
            key="api_key_input_main",
            label_visibility="collapsed"
        )

    with col2:
        # 保存按钮
        if st.button("保存", key="save_api_key", use_container_width=True):
            if api_key_input:
                is_valid, error_msg = validate_api_key(api_key_input)
                if is_valid:
                    st.session_state.saved_api_key = api_key_input
                    st.session_state.api_key = api_key_input
                    st.success("✓ API Key 已保存")

                    # 使用JavaScript保存到localStorage
                    st.markdown(f"""
                    <script>
                        localStorage.setItem('nano_banana_api_key', '{api_key_input}');
                    </script>
                    """, unsafe_allow_html=True)
                else:
                    st.error(f"✗ {error_msg}")
            else:
                st.warning("请先输入 API Key")

    # 显示状态
    if st.session_state.get('saved_api_key'):
        st.markdown('<div class="api-status api-status-success">✓ 已配置</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="api-status api-status-warning">未配置 API Key</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


def render_sidebar():
    """渲染侧边栏 - 极简风格"""
    with st.sidebar:
        st.markdown("## 图标生成系统")
        st.markdown("---")

        # 使用说明
        st.markdown("### 使用流程")
        st.markdown("""
        1. 配置 API Key
        2. 输入图标名称
        3. 选择视觉风格
        4. 调整参数设置
        5. 生成并下载
        """)

        st.markdown("---")

        # 支持的风格
        st.markdown("### 可用风格")
        st.markdown("""
        - 3D黏土风
        - 霓虹赛博朋克
        - 极简毛玻璃
        - 扁平渐变
        - 拟物厚涂
        - 更多...
        """)

        st.markdown("---")

        # 关于
        st.markdown("### 关于")
        st.markdown("""
        **版本**: 1.0.0
        **技术**: Streamlit + Nano Banana API

        [获取 API Key](https://kie.ai/api-key)
        """)

        # 底部版权
        st.markdown("---")
        st.markdown(
            "<div style='text-align: center; color: #999; font-size: 0.85rem;'>© 2026 UI Icon Generator</div>",
            unsafe_allow_html=True
        )


def render_icon_input():
    """渲染图标输入区域"""
    st.markdown('<div class="step-header">📝 步骤 1 · 输入图标清单</div>', unsafe_allow_html=True)

    icon_text = st.text_area(
        label="图标清单",
        placeholder="例如：主页, 购物车, 设置, 个人中心, 搜索",
        help="输入需要生成的图标名称，用逗号分隔，支持 1-10 个图标",
        height=100,
        label_visibility="collapsed"
    )

    # 验证输入
    if icon_text:
        is_valid, error_msg, icon_list = validate_icon_list(icon_text)
        if not is_valid:
            st.error(f"✗ {error_msg}")
            return None
        else:
            st.success(f"✓ 已识别 {len(icon_list)} 个图标：{', '.join(icon_list)}")
            return icon_list

    return None


def render_style_selection(style_mapper: StyleMapper):
    """渲染风格选择区域"""
    st.markdown('<div class="step-header">🎨 步骤 2 · 选择视觉风格</div>', unsafe_allow_html=True)

    # 获取所有风格
    styles = style_mapper.list_available_styles()
    style_names = [name for name, _ in styles]

    # 风格选择
    selected_style = st.selectbox(
        label="视觉风格",
        options=style_names,
        help="选择图标的视觉风格",
        label_visibility="collapsed"
    )

    # 显示风格预览
    if selected_style:
        style_components = style_mapper.get_style_components(selected_style)
        if style_components:
            with st.expander("查看风格详情"):
                st.markdown(f"**{style_components.description}**")
                st.markdown("")
                st.markdown(f"**风格定义**：{style_components.medium}")
                st.markdown(f"**材质描述**：{style_components.material}")
                st.markdown(f"**光影效果**：{style_components.lighting}")
                st.markdown(f"**背景设置**：{style_components.background}")

    return selected_style


def render_advanced_settings():
    """渲染高级设置"""
    st.markdown('<div class="step-header">⚙️ 步骤 3 · 参数设置</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        resolution = st.selectbox(
            "分辨率",
            options=["1K", "2K", "4K"],
            index=0,
            help="分辨率越高，生成时间越长"
        )

    with col2:
        aspect_ratio = st.selectbox(
            "宽高比",
            options=["1:1", "16:9", "4:3", "3:2", "9:16"],
            index=1
        )

    with col3:
        output_format = st.selectbox(
            "输出格式",
            options=["png", "jpg"],
            index=0
        )

    return resolution, aspect_ratio, output_format


def render_prompt_preview(prompt: str):
    """渲染提示词预览"""
    if prompt:
        st.markdown("")
        st.markdown("### 生成的提示词")
        st.code(prompt, language="text")


async def generate_icons_async(
    icon_list,
    style_name,
    prompt_generator,
    api_key,
    resolution,
    aspect_ratio,
    output_format
):
    """异步生成图标"""
    # 生成提示词
    success, result, used_style = prompt_generator.generate(
        icon_list=icon_list,
        style_name=style_name,
        aspect_ratio=aspect_ratio
    )

    if not success:
        st.error(f"❌ {result}")
        return None, None

    prompt = result
    st.session_state.current_prompt = prompt

    # 显示提示词预览
    render_prompt_preview(prompt)

    # 创建生成任务
    tasks = [
        GenerationTask(icon_name=icon, prompt=prompt)
        for icon in icon_list
    ]

    # 创建进度显示
    progress_bar = st.progress(0)
    status_text = st.empty()

    try:
        # 初始化客户端和任务管理器
        async with NanoBananaClient(api_key=api_key) as client:
            task_manager = TaskManager(client=client, max_concurrent=3)

            # 进度回调
            def update_progress(completed, total, current_icon):
                progress = completed / total
                progress_bar.progress(progress)
                status_text.text(f"⏳ 正在生成: {current_icon} ({completed}/{total})")

            # 批量生成
            tasks = await task_manager.batch_generate(
                tasks=tasks,
                max_wait=300,
                aspect_ratio=aspect_ratio,
                resolution=resolution,
                output_format=output_format,
                progress_callback=update_progress
            )

            # 下载结果
            status_text.text("📥 正在下载结果...")
            output_dir = settings.output_path / datetime.now().strftime("%Y%m%d_%H%M%S")
            output_dir.mkdir(parents=True, exist_ok=True)

            downloaded_files = await task_manager.download_results(
                tasks=tasks,
                output_dir=output_dir
            )

            progress_bar.progress(1.0)
            status_text.text("✅ 生成完成！")

            return tasks, downloaded_files

    except AuthenticationError:
        st.error("❌ 认证失败，请检查 API Key 是否正确")
    except InsufficientBalanceError:
        st.error("❌ 账户余额不足，请充值后重试")
    except RateLimitError:
        st.error("❌ 请求过于频繁，请稍后重试")
    except Exception as e:
        st.error(f"❌ 生成失败: {str(e)}")

    return None, None


def render_results(tasks, downloaded_files):
    """渲染生成结果"""
    if not tasks or not downloaded_files:
        return

    st.markdown("")
    st.markdown("")
    st.markdown("## 生成结果")

    # 统计信息
    success_count = sum(1 for t in tasks if t.result and t.result.is_success)
    failed_count = len(tasks) - success_count

    col1, col2, col3 = st.columns(3)
    col1.metric("总计", len(tasks))
    col2.metric("成功", success_count)
    col3.metric("失败", failed_count)

    # 显示图标网格
    st.markdown("")
    st.markdown("### 图标预览")

    # 3列网格布局
    cols = st.columns(3)

    for idx, file_path in enumerate(downloaded_files):
        with cols[idx % 3]:
            try:
                image = Image.open(file_path)
                st.image(image, caption=file_path.stem, use_container_width=True)

                # 下载按钮
                with open(file_path, 'rb') as f:
                    st.download_button(
                        label="下载",
                        data=f.read(),
                        file_name=file_path.name,
                        mime="image/png",
                        key=f"download_{idx}",
                        use_container_width=True
                    )
            except Exception as e:
                st.error(f"✗ 加载图片失败: {e}")

    # 批量下载
    if len(downloaded_files) > 1:
        st.markdown("")
        st.markdown("### 批量下载")

        # 创建ZIP文件
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for file_path in downloaded_files:
                zip_file.write(file_path, file_path.name)

        zip_buffer.seek(0)

        st.download_button(
            label="下载全部图标 (ZIP)",
            data=zip_buffer.getvalue(),
            file_name=f"icons_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip",
            mime="application/zip"
        )


def main():
    """主函数"""
    # 初始化
    init_session_state()

    # 渲染侧边栏
    render_sidebar()

    # API设置卡片（页面最顶部）
    render_api_settings_card()

    # 主标题 - 极简风格
    st.markdown('<h1 class="main-header">UI 图标生成器</h1>', unsafe_allow_html=True)
    st.markdown('<p class="main-subtitle">基于 AI 的专业图标生成工具，一键创建多种风格的 UI 图标</p>', unsafe_allow_html=True)

    # 初始化组件
    style_mapper = StyleMapper()
    prompt_generator = PromptGenerator(style_mapper=style_mapper)

    # 步骤 1: 输入图标清单
    icon_list = render_icon_input()

    # 步骤 2: 选择风格
    if icon_list:
        selected_style = render_style_selection(style_mapper)

        # 步骤 3: 高级设置
        resolution, aspect_ratio, output_format = render_advanced_settings()

        # 生成按钮区域
        st.markdown("")  # 添加间距
        col1, col2 = st.columns([1, 1])

        with col1:
            if st.button("生成图标", type="primary", use_container_width=True):
                # 优先使用API设置卡片中保存的Key，然后是侧边栏的Key
                api_key = st.session_state.get('saved_api_key', '') or st.session_state.get('api_key', '')

                if not api_key:
                    st.error("✗ 请先配置 API Key")
                else:
                    # 验证API Key
                    is_valid, error_msg = validate_api_key(api_key)
                    if not is_valid:
                        st.error(f"✗ {error_msg}")
                    else:
                        # 异步生成
                        tasks, downloaded_files = asyncio.run(
                            generate_icons_async(
                                icon_list=icon_list,
                                style_name=selected_style,
                                prompt_generator=prompt_generator,
                                api_key=api_key,
                                resolution=resolution,
                                aspect_ratio=aspect_ratio,
                                output_format=output_format
                            )
                        )

                        # 保存到会话状态
                        if tasks:
                            st.session_state.generated_tasks = tasks
                            st.session_state.downloaded_files = downloaded_files

        with col2:
            # 预览提示词按钮
            if st.button("预览提示词", use_container_width=True):
                success, result, used_style = prompt_generator.generate(
                    icon_list=icon_list,
                    style_name=selected_style,
                    aspect_ratio=aspect_ratio
                )
                if success:
                    st.session_state.current_prompt = result
                else:
                    st.error(f"✗ {result}")

        # 显示当前提示词预览
        if st.session_state.current_prompt:
            render_prompt_preview(st.session_state.current_prompt)

    # 显示结果
    if 'downloaded_files' in st.session_state and st.session_state.downloaded_files:
        render_results(
            st.session_state.generated_tasks,
            st.session_state.downloaded_files
        )


if __name__ == "__main__":
    main()
