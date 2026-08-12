# 答案自动补全工具

[English](./README_EN.md)

一个面向 Excel 问卷/访谈数据的答案自动补全工具。它会扫描指定文件夹中的 `.xlsx` / `.xlsm`，识别第 2 行里明显无效的答案，并调用本地 OpenAI 兼容大模型接口生成更自然、更完整的回答，最后把结果写入新的输出文件，原始表格不会被修改。

如果你也经常遇到“问卷答案里混着空值、单个字母、乱填数字”的情况，这个小工具就是为这类脏活准备的。欢迎 Star、Fork、提 Issue，一起把它打磨成更顺手的 AI 数据清洗助手。

## 功能亮点

- Excel 批处理：支持扫描文件夹内的 `.xlsx` 和 `.xlsm` 文件。
- 原文件保护：先复制再写入，补全结果输出到 `answer_autofill_output`。
- 问卷结构适配：默认读取第 1 行题目、第 2 行答案，从 `AS` 列开始每 5 列作为一个题组。
- 上下文补全：会读取 `G/H/I/K/M/W/AH/AO` 等基础信息，并把同组已有有效答案作为参考。
- 异步并发：默认并发数为 `8`，适合本地大模型服务批量处理。
- 干跑扫描：`--dry-run` 只统计无效答案，不调用模型、不生成文件。
- 冒烟测试：`--smoke-test` 可先用真实接口测试一个题组，避免大批量跑错。
- 配置灵活：支持 `config.json` 和环境变量覆盖模型地址、API Key、模型名等。

## 技术栈

- Python 3.11+
- openpyxl
- OpenAI Python SDK
- httpx / asyncio / tqdm
- OpenAI-compatible Chat Completions API

## 快速开始

### 1. 准备模型服务

默认连接本地 OpenAI 兼容接口：

```text
Base URL: http://127.0.0.1:8008/v1
API Key: test
Model: deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B
```

请先启动你的本地模型服务，并确认 `/chat/completions` 可用。

### 2. 安装依赖

Windows 用户可以直接运行：

```powershell
.\setup_env.ps1
```

也可以手动创建环境：

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 3. 扫描无效答案

```powershell
python -m answer_autofill "D:\path\to\excel_folder" --dry-run
```

### 4. 正式补全

```powershell
python -m answer_autofill "D:\path\to\excel_folder"
```

或使用脚本：

```powershell
.\start.ps1 "D:\path\to\excel_folder"
```

输出文件会生成在输入文件夹下的 `answer_autofill_output` 目录。

## 常用参数

```powershell
python -m answer_autofill "D:\path\to\excel_folder" `
  --config ".\config.json" `
  --output-dir "D:\path\to\output" `
  --concurrency 8
```

- `--dry-run`：只扫描统计，不调用模型。
- `--smoke-test`：只请求第一个包含无效值的题组。
- `--smoke-column BR`：指定冒烟测试列。
- `--recursive`：递归处理子文件夹。
- `--output-dir`：指定输出目录。
- `--concurrency`：设置并发请求数。

## 配置说明

默认配置在 [config.json](./config.json)：

```json
{
  "model": {
    "base_url": "http://127.0.0.1:8008/v1",
    "api_key": "test",
    "model": "deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B"
  }
}
```

也可以使用环境变量覆盖：

- `ANSWER_AUTOFILL_BASE_URL`
- `ANSWER_AUTOFILL_API_KEY`
- `ANSWER_AUTOFILL_MODEL`

## 无效答案规则

默认认为以下内容需要补全：

- 空值
- 单个数字或字母，例如 `1`、`a`
- 全部由标点或符号组成的内容

类似“想不起来”“不清楚”“没有相关想法”这类自然语言内容会被保留，不会被强行覆盖。

## 项目结构

```text
answer_autofill/
├─ answer_autofill/        # 核心源码
├─ excle_deal/             # 可放本地待处理 Excel，上传仓库时建议排除数据文件
├─ config.json             # 默认配置
├─ requirements.txt
├─ setup_env.ps1
├─ start.ps1
└─ README.md
```

## 上传 GitHub 前建议

不要上传个人数据、生成结果、缓存文件和日志。本项目已经提供 `.gitignore`，重点会排除：

- `__pycache__/`
- `.venv/`
- `logs/`
- `*.xlsx` / `*.xlsm`
- `answer_autofill_output/`

如果你需要保留示例表格，建议放一个脱敏后的 `sample.xlsx`，并确认里面没有真实个人信息。

## GitHub Topics 建议

`python`, `excel`, `openpyxl`, `llm`, `deepseek`, `openai-compatible`, `data-cleaning`, `survey-data`, `automation`, `chinese`

## 适用场景

- 问卷答案清洗
- Excel 缺失文本补全
- 本地大模型批处理验证
- 访谈/调研数据预处理
- AI 办公自动化小工具

## License

如果你准备开源，建议选择 MIT License，方便更多人使用和二次开发。
