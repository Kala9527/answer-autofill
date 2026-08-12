# Answer Autofill Tool

[中文说明](./README.md)

An Excel answer autofill utility for survey and interview data. It scans `.xlsx` / `.xlsm` files, detects obviously invalid answers in row 2, calls a local OpenAI-compatible LLM service, and writes completed answers into a new output workbook while keeping the original files unchanged.

If your spreadsheet has empty cells, single-letter placeholders, or quick numeric throwaway answers, this tool can help turn that cleanup work into a repeatable AI-assisted workflow. Stars, forks, and issues are warmly welcome.

## Highlights

- Batch Excel processing for `.xlsx` and `.xlsm` files.
- Safe output workflow: source files are copied first, then completed files are written to `answer_autofill_output`.
- Survey-oriented layout: reads questions from row 1, answers from row 2, and groups question columns from `AS` onward in blocks of 5.
- Context-aware generation: uses configured basic information columns and valid answers in the same group as context.
- Async model requests with default concurrency of `8`.
- `--dry-run` mode for scanning invalid answers without model calls.
- `--smoke-test` mode for testing one real request before running a full batch.
- Configurable through `config.json` and environment variables.

## Tech Stack

- Python 3.11+
- openpyxl
- OpenAI Python SDK
- httpx / asyncio / tqdm
- OpenAI-compatible Chat Completions API

## Quick Start

### 1. Start an LLM service

Default local endpoint:

```text
Base URL: http://127.0.0.1:8008/v1
API Key: test
Model: deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B
```

Make sure your model service supports `/chat/completions`.

### 2. Install dependencies

On Windows:

```powershell
.\setup_env.ps1
```

Or use a standard virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 3. Scan only

```powershell
python -m answer_autofill "D:\path\to\excel_folder" --dry-run
```

### 4. Run autofill

```powershell
python -m answer_autofill "D:\path\to\excel_folder"
```

Or:

```powershell
.\start.ps1 "D:\path\to\excel_folder"
```

Completed workbooks are written to `answer_autofill_output` under the input folder by default.

## Common Options

```powershell
python -m answer_autofill "D:\path\to\excel_folder" `
  --config ".\config.json" `
  --output-dir "D:\path\to\output" `
  --concurrency 8
```

- `--dry-run`: scan only, no model calls.
- `--smoke-test`: test the first invalid question group.
- `--smoke-column BR`: smoke-test a specific column.
- `--recursive`: process subfolders.
- `--output-dir`: choose an output folder.
- `--concurrency`: set maximum concurrent model requests.

## Configuration

Default settings are stored in [config.json](./config.json):

```json
{
  "model": {
    "base_url": "http://127.0.0.1:8008/v1",
    "api_key": "test",
    "model": "deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B"
  }
}
```

Environment overrides:

- `ANSWER_AUTOFILL_BASE_URL`
- `ANSWER_AUTOFILL_API_KEY`
- `ANSWER_AUTOFILL_MODEL`

## Invalid Answer Rules

The tool autofills:

- Empty values
- Single numbers or letters, such as `1` or `a`
- Values made only of punctuation or symbols

Natural language answers such as "not sure" or "cannot remember" are preserved.

## GitHub Topics

`python`, `excel`, `openpyxl`, `llm`, `deepseek`, `openai-compatible`, `data-cleaning`, `survey-data`, `automation`, `chinese`

## License

MIT License is recommended if you plan to publish this project as open source.
