# 🚀 快速启动指南

## 前置要求

1. ✅ Python 3.8+ 已安装
2. ✅ 有可用的网络连接
3. ✅ Nano Banana API Key（[获取地址](https://kie.ai/api-key)）

## 方法 1: 一键启动（推荐）

```bash
# 1. 安装依赖（仅首次运行需要）
pip3 install streamlit httpx tenacity pydantic pydantic-settings python-dotenv pyyaml jinja2 loguru pillow tqdm

# 2. 配置 API Key（可选，也可以在UI中输入）
cp .env.example .env
# 编辑 .env 文件，填入你的 API Key

# 3. 启动应用
python3 run.py
```

应用将自动在浏览器打开: http://localhost:8501

## 方法 2: 使用 Streamlit 命令

```bash
# 安装依赖
pip3 install -r requirements.txt

# 启动应用
streamlit run src/ui/app.py
```

## 方法 3: 仅测试核心功能（不启动Web界面）

```bash
# 运行示例脚本
python3 example.py
```

## 首次使用步骤

### 1. 在侧边栏输入 API Key

如果没有在 `.env` 文件配置，请在应用侧边栏的"API 配置"区域输入你的 API Key。

### 2. 输入图标清单

在"步骤 1"区域输入需要生成的图标，例如：

```
主页, 购物车, 设置, 个人中心
```

### 3. 选择视觉风格

从"步骤 2"的下拉框中选择风格，例如：

- 3D黏土风（可爱清新）
- 霓虹赛博朋克（科技未来）
- 极简毛玻璃（现代简约）

### 4. 配置参数（可选）

在"步骤 3"设置：
- 分辨率：1K（快速）/ 2K（均衡）/ 4K（高质量）
- 宽高比：16:9（横向）/ 1:1（方形）等
- 输出格式：PNG（推荐）/ JPG

### 5. 生成图标

- 点击"预览提示词"查看将要发送的提示词
- 点击"开始生成图标"提交任务
- 等待生成完成（实时显示进度）

### 6. 下载结果

- 单个下载：点击每个图标下方的"下载"按钮
- 批量下载：点击"下载全部图标（ZIP）"

## 测试系统是否正常

运行快速测试：

```bash
python3 -c "
from src.core.style_mapper import StyleMapper
from src.core.prompt_generator import PromptGenerator

mapper = StyleMapper()
generator = PromptGenerator(mapper)

success, prompt, style = generator.generate(
    icon_list=['主页', '设置'],
    style_name='3D黏土风'
)

if success:
    print('✅ 系统正常！')
    print(f'生成的提示词长度: {len(prompt)} 字符')
else:
    print('❌ 系统异常: ' + prompt)
"
```

如果看到 `✅ 系统正常！` 则表示核心功能工作正常。

## 常见问题

### Q1: 提示 "Module not found"

**解决方案**：
```bash
pip3 install -r requirements.txt
```

### Q2: 端口 8501 被占用

**解决方案**：
```bash
streamlit run src/ui/app.py --server.port 8502
```

### Q3: API Key 无效

**解决方案**：
1. 访问 https://kie.ai/api-key 确认 API Key
2. 确保没有多余的空格
3. 重新输入或更新 `.env` 文件

### Q4: 生成速度慢

**解决方案**：
1. 使用 1K 分辨率（最快）
2. 减少图标数量
3. 检查网络连接

## 目录结构说明

```
图标生成/
├── src/              # 源代码
├── config/           # 配置文件（风格、翻译等）
├── data/generated/   # 生成的图标保存位置
├── logs/             # 日志文件
├── example.py        # 使用示例
├── run.py            # 启动脚本
└── README.md         # 完整文档
```

## 下一步

- 📖 阅读 [README.md](README.md) 了解完整功能
- 🎨 查看 [config/styles.yaml](config/styles.yaml) 了解可用风格
- 🔧 编辑 [config/icon_translations.yaml](config/icon_translations.yaml) 添加自定义翻译

## 获取帮助

- 查看完整文档: `README.md`
- 运行示例代码: `python3 example.py`
- 查看日志文件: `logs/app_*.log`

---

**祝使用愉快！** 🎨✨
