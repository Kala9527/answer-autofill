from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any


DEFAULT_CONFIG: dict[str, Any] = {
    "model": {
        "base_url": "http://127.0.0.1:8008/v1",
        "api_key": "test",
        "model": "deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B",
        "temperature": 0.2,
        "max_tokens": 1200,
        "timeout_seconds": 300,
        "retries": 2,
    },
    "excel": {
        "header_row": 1,
        "answer_row": 2,
        "basic_info_cols": ["G", "H", "I", "K", "M", "W", "AH", "AO"],
        "question_group_start_col": "AS",
        "question_group_size": 5,
        "occupation_col": "K",
    },
    "processing": {
        "output_dir_name": "answer_autofill_output",
        "recursive": False,
        "skip_output_folders": True,
        "concurrency": 8,
    },
}


@dataclass(frozen=True)
class ModelConfig:
    base_url: str
    api_key: str
    model: str
    temperature: float
    max_tokens: int
    timeout_seconds: int
    retries: int


@dataclass(frozen=True)
class ExcelConfig:
    header_row: int
    answer_row: int
    basic_info_cols: tuple[str, ...]
    question_group_start_col: str
    question_group_size: int
    occupation_col: str


@dataclass(frozen=True)
class ProcessingConfig:
    output_dir_name: str
    recursive: bool
    skip_output_folders: bool
    concurrency: int


@dataclass(frozen=True)
class AppConfig:
    model: ModelConfig
    excel: ExcelConfig
    processing: ProcessingConfig


def load_config(path: Path | None = None) -> AppConfig:
    raw = json.loads(json.dumps(DEFAULT_CONFIG, ensure_ascii=False))
    if path and path.exists():
        with path.open("r", encoding="utf-8") as handle:
            raw = _deep_merge(raw, json.load(handle))

    _apply_env_overrides(raw)

    model = raw["model"]
    excel = raw["excel"]
    processing = raw["processing"]

    return AppConfig(
        model=ModelConfig(
            base_url=str(model["base_url"]).rstrip("/"),
            api_key=str(model.get("api_key", "")),
            model=str(model["model"]),
            temperature=float(model["temperature"]),
            max_tokens=int(model["max_tokens"]),
            timeout_seconds=int(model["timeout_seconds"]),
            retries=max(1, int(model["retries"])),
        ),
        excel=ExcelConfig(
            header_row=int(excel["header_row"]),
            answer_row=int(excel["answer_row"]),
            basic_info_cols=tuple(str(item).upper() for item in excel.get("basic_info_cols", ("G", "H", "I", "K", "M", "W", "AH", "AO"))),
            question_group_start_col=str(excel["question_group_start_col"]).upper(),
            question_group_size=int(excel["question_group_size"]),
            occupation_col=str(excel["occupation_col"]).upper(),
        ),
        processing=ProcessingConfig(
            output_dir_name=str(processing["output_dir_name"]),
            recursive=bool(processing["recursive"]),
            skip_output_folders=bool(processing["skip_output_folders"]),
            concurrency=max(1, int(processing.get("concurrency", 8))),
        ),
    )


def _deep_merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(base.get(key), dict):
            _deep_merge(base[key], value)
        else:
            base[key] = value
    return base


def _apply_env_overrides(raw: dict[str, Any]) -> None:
    env_map = {
        "ANSWER_AUTOFILL_BASE_URL": ("model", "base_url"),
        "ANSWER_AUTOFILL_API_KEY": ("model", "api_key"),
        "ANSWER_AUTOFILL_MODEL": ("model", "model"),
        "ANSWER_AUTOFILL_TEMPERATURE": ("model", "temperature"),
        "ANSWER_AUTOFILL_MAX_TOKENS": ("model", "max_tokens"),
        "ANSWER_AUTOFILL_TIMEOUT": ("model", "timeout_seconds"),
    }
    for env_name, path in env_map.items():
        value = os.getenv(env_name)
        if value not in (None, ""):
            raw[path[0]][path[1]] = value
