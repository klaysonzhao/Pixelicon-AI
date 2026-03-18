"""
API设置卡片使用指南
===================

快速开始：
1. 运行: python3 run.py
2. 在页面顶部紫色卡片输入 API Key
3. 点击"保存"按钮
4. 开始生成图标

功能说明：
- 输入框会保存 API Key 到会话和浏览器存储
- 刷新页面后仍然有效（存储在 localStorage）
- 优先使用此处保存的 Key

测试浏览器存储：
打开浏览器控制台（F12），输入：
  localStorage.getItem('nano_banana_api_key')

清除存储：
  localStorage.removeItem('nano_banana_api_key')
"""

print(__doc__)
