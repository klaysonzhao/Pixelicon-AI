#!/usr/bin/env python3
"""UI 图标生成系统 - 启动脚本"""
import sys
import subprocess
from pathlib import Path


def check_requirements():
    """检查依赖是否已安装"""
    try:
        import streamlit
        return True
    except ImportError:
        return False


def main():
    """主函数"""
    # 切换到项目根目录
    project_root = Path(__file__).parent
    sys.path.insert(0, str(project_root))

    # 检查依赖
    if not check_requirements():
        print("⚠️  检测到缺少依赖，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

    # 启动 Streamlit 应用
    print("🚀 启动 UI 图标生成系统...")
    subprocess.run([
        sys.executable, "-m", "streamlit", "run",
        str(project_root / "src" / "ui" / "app.py"),
        "--server.address", "localhost",
        "--server.port", "8501",
        "--browser.gatherUsageStats", "false"
    ])


if __name__ == "__main__":
    main()
