# 🎨 UI 风格化图标生成系统

基于 AI 的专业 UI 图标生成工具，支持多种视觉风格。通过简单的交互界面，输入图标需求和选择风格，即可快速生成高质量的 UI 图标。

## ✨ 特性

- 🎯 **简单易用**: 交互式 Web 界面，无需编程知识
- 🎨 **多种风格**: 支持 10+ 种预设视觉风格（3D黏土、霓虹赛博朋克、毛玻璃等）
- 🚀 **批量生成**: 一次生成多个图标，自动并发处理
- 📥 **便捷下载**: 支持单个下载或批量打包下载
- 🔄 **智能翻译**: 自动将中文图标名称翻译为专业英文提示词
- ⚡ **实时反馈**: 显示生成进度和任务状态

## 🎨 支持的风格

- **3D黏土风**: 可爱的3D黏土质感，圆润饱满，柔和色彩
- **霓虹赛博朋克**: 未来科技感，霓虹发光线条，高对比度
- **极简毛玻璃**: 现代毛玻璃质感，半透明渐变，轻盈优雅
- **扁平渐变**: 扁平设计风格，渐变色彩，简洁现代
- **拟物厚涂**: 拟真材质，立体厚重，细节丰富
- **线性艺术**: 极简线条艺术，单色或双色，优雅流畅
- **水彩手绘**: 水彩插画风格，手绘质感，柔和自然
- **金属质感**: 高端金属质感，奢华精致，反光效果
- **等距3D**: 等距视角3D，几何精确，色块分明
- **渐变网格**: 渐变网格，流体形态，彩虹色过渡

## 📋 系统要求

- Python 3.8+
- 网络连接（调用 Nano Banana API）
- Nano Banana API Key（在 [kie.ai](https://kie.ai/api-key) 获取）

## 🚀 快速开始

### 1. 克隆或下载项目

```bash
cd /path/to/图标生成
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置 API Key

复制环境变量模板：

```bash
cp .env.example .env
```

编辑 `.env` 文件，填入你的 API Key：

```env
NANO_BANANA_API_KEY=your_api_key_here
```

> 💡 **提示**: 也可以在应用启动后，通过侧边栏输入 API Key（不会保存到文件）

### 4. 启动应用

```bash
python run.py
```

或直接使用 Streamlit：

```bash
streamlit run src/ui/app.py
```

应用将自动在浏览器打开（默认地址: `http://localhost:8501`）

## 📖 使用指南

### 基本流程

1. **输入图标清单**
   - 在文本框输入需要生成的图标名称
   - 用逗号、顿号或中文逗号分隔
   - 示例: `主页, 购物车, 设置, 个人中心, 搜索`
   - 支持 1-10 个图标

2. **选择视觉风格**
   - 从下拉框选择预设风格
   - 点击"风格详情"查看风格说明
   - 系统自动匹配对应的 AI 提示词组件

3. **配置高级参数（可选）**
   - **分辨率**: 1K（快速）/ 2K（均衡）/ 4K（高质量）
   - **宽高比**: 1:1, 16:9, 4:3 等
   - **输出格式**: PNG（推荐）/ JPG

4. **生成图标**
   - 点击"预览提示词"查看生成的 AI 提示词
   - 点击"开始生成图标"提交任务
   - 实时查看生成进度和状态

5. **下载结果**
   - 单个下载：点击每个图标下方的"下载"按钮
   - 批量下载：点击"下载全部图标（ZIP）"

### 高级功能

#### 自定义图标翻译

编辑 `config/icon_translations.yaml` 添加自定义翻译：

```yaml
我的图标: "a custom icon description"
```

#### 添加自定义风格

编辑 `config/styles.yaml` 添加新风格：

```yaml
styles:
  我的风格:
    medium: "风格媒介描述"
    material: "材质描述"
    lighting: "光影描述"
    background: "背景描述"
    description: "中文描述"
```

## 📁 项目结构

```
图标生成/
├── src/
│   ├── api/              # API 客户端
│   │   ├── client.py     # Nano Banana API 封装
│   │   └── models.py     # 数据模型
│   ├── core/             # 核心业务逻辑
│   │   ├── style_mapper.py      # 风格映射
│   │   ├── prompt_generator.py  # 提示词生成
│   │   └── task_manager.py      # 任务管理
│   ├── ui/               # 用户界面
│   │   └── app.py        # Streamlit 主应用
│   └── utils/            # 工具模块
│       ├── config.py     # 配置管理
│       ├── logger.py     # 日志工具
│       └── validators.py # 输入验证
├── config/               # 配置文件
│   ├── styles.yaml       # 风格配置
│   ├── icon_translations.yaml  # 图标翻译
│   └── settings.yaml     # 应用设置
├── data/
│   └── generated/        # 生成的图标存储
├── ai-docs/              # API 文档
├── prompot.md            # 提示词生成规则
├── requirements.txt      # 依赖列表
├── run.py                # 启动脚本
└── README.md             # 本文档
```

## 🔧 配置说明

### 环境变量（`.env`）

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| `NANO_BANANA_API_KEY` | API Key（必填） | - |
| `NANO_BANANA_BASE_URL` | API 地址 | `https://api.kie.ai/api/v1` |
| `LOG_LEVEL` | 日志级别 | `INFO` |
| `MAX_CONCURRENT_TASKS` | 最大并发数 | `3` |
| `DEFAULT_TIMEOUT` | 超时时间（秒） | `300` |
| `POLL_INTERVAL` | 轮询间隔（秒） | `3` |
| `OUTPUT_DIR` | 输出目录 | `./data/generated` |

### 应用设置（`config/settings.yaml`）

```yaml
api:
  retry_attempts: 3      # API 重试次数
  retry_backoff: 2       # 重试退避因子
  timeout: 30            # 请求超时

generation:
  default_resolution: "1K"
  default_aspect_ratio: "16:9"
  default_output_format: "png"
  max_icons_per_batch: 10

ui:
  show_advanced_options: true
  enable_history: false
```

## 🐛 故障排查

### 问题 1: 认证失败

**错误**: `❌ 认证失败，请检查 API Key 是否正确`

**解决方案**:
1. 确认 API Key 已正确配置（`.env` 或侧边栏输入）
2. 前往 https://kie.ai/api-key 验证 API Key 是否有效
3. 检查 API Key 前后是否有多余空格

### 问题 2: 账户余额不足

**错误**: `❌ 账户余额不足，请充值后重试`

**解决方案**:
1. 登录 https://kie.ai 查看账户余额
2. 充值后重试

### 问题 3: 请求过于频繁

**错误**: `❌ 请求过于频繁，请稍后重试`

**解决方案**:
1. 等待几分钟后重试
2. 减少并发任务数（修改 `.env` 中的 `MAX_CONCURRENT_TASKS`）

### 问题 4: 生成超时

**错误**: `任务超时 (300秒)`

**解决方案**:
1. 增加超时时间（修改 `.env` 中的 `DEFAULT_TIMEOUT`）
2. 降低分辨率（使用 1K 代替 4K）
3. 检查网络连接是否稳定

### 问题 5: 依赖安装失败

**解决方案**:
```bash
# 升级 pip
pip install --upgrade pip

# 清理缓存重新安装
pip cache purge
pip install -r requirements.txt --no-cache-dir
```

## 📊 性能说明

- **1K 分辨率**: 通常 30-60 秒/图标（推荐）
- **2K 分辨率**: 通常 60-120 秒/图标
- **4K 分辨率**: 通常 120-300 秒/图标

> 💡 实际生成时间取决于 API 服务器负载和网络状况

## 🔐 安全提示

- ⚠️ **不要**将 `.env` 文件提交到版本控制系统
- ⚠️ **不要**在公开场合分享你的 API Key
- ✅ 使用环境变量或配置文件管理敏感信息
- ✅ 定期更换 API Key

## 📝 开发说明

### 运行测试

```bash
pytest tests/ -v
```

### 查看日志

日志文件位于 `logs/` 目录，按日期自动分割：

```bash
tail -f logs/app_2026-03-19.log
```

### 添加新风格

1. 编辑 `config/styles.yaml`
2. 按照现有格式添加新风格
3. 重启应用即可使用

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

## 🙏 致谢

- [Streamlit](https://streamlit.io/) - Web 应用框架
- [Nano Banana API](https://kie.ai/) - AI 图像生成服务
- [Loguru](https://github.com/Delgan/loguru) - 日志库

## 📞 联系方式

如有问题或建议，欢迎通过以下方式联系：

- 提交 GitHub Issue
- 发送邮件至开发者

---

**享受创作！** 🎨✨
