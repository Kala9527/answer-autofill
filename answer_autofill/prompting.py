from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class QAItem:
    column: str
    question: str
    answer: str


@dataclass(frozen=True)
class TargetItem:
    column: str
    question: str
    original_answer: str


def build_cell_messages(
    *,
    basic_info: list[QAItem],
    group_items: list[QAItem],
    context_answers: list[QAItem],
    target: TargetItem,
) -> list[dict[str, str]]:
    system = "你是雅思口语答案补全助手。你只输出一个中文答案正文。"
    user = "\n".join(
        [
            "任务：补全一个雅思口语答案单元格。",
            "输出规则：只写答案正文；不要列字母；不要题号；不要复述题目；不要JSON；不要解释。",
            "答案长度：1到2句中文。",
            "事实规则：不能违背基础信息；K列职业中1表示工作，2表示学生。",
            "连贯规则：同组参考答案是事实，包括前面刚补全的新答案。",
            "低信息规则：如果参考答案表示没想法、不清楚、想不起来或没有印象，要延续这个口径，不要编造成具体真实经历。",
            "",
            _format_items("基础信息", basic_info, include_column=False),
            "",
            _format_items("同组题目和当前答案", group_items, include_column=False),
            "",
            _format_items("同组参考答案", context_answers, include_column=False),
            "",
            f"要回答的问题：{_strip_question_number(target.question)}",
            "",
            "直接给出答案正文：",
        ]
    )
    return [{"role": "system", "content": system}, {"role": "user", "content": user}]


def clean_plain_answer(content: Any) -> str:
    text = str(content or "").strip()
    text = _strip_thinking(text)
    text = text.strip()
    text = re.sub(r"^```(?:text|markdown|json)?", "", text, flags=re.I).strip()
    text = re.sub(r"```$", "", text).strip()
    text = text.strip("\"'“”‘’")
    text = _remove_question_echo(text)
    text = re.sub(r"^\s*(答案|补全答案|最终答案)\s*[:：]\s*", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return _limit_sentences(text, max_sentences=2)


def _format_items(title: str, items: list[QAItem], *, include_column: bool = True) -> str:
    if not items:
        return f"{title}：无"
    lines = [f"{title}："]
    for item in items:
        question = _strip_question_number(item.question)
        prefix = f"{item.column} | " if include_column else ""
        lines.append(f"- {prefix}{question}：{item.answer}")
    return "\n".join(lines)


def _strip_thinking(content: str) -> str:
    return re.sub(r"<think>.*?</think>", "", content, flags=re.S | re.I)


def _remove_question_echo(text: str) -> str:
    cleaned = text.strip()
    cleaned = re.sub(r"^[A-Z]{1,3}\s*\|\s*[^。！？!?]*[。！？!?]?\s*", "", cleaned)
    cleaned = re.sub(r"^[A-Z]{1,3}\s*[：:]\s*", "", cleaned)
    parts = [part.strip() for part in re.split(r"(?<=[。！？!?])\s*", cleaned) if part.strip()]
    if len(parts) >= 2 and parts[0] == parts[1]:
        return parts[0]
    return cleaned


def _strip_question_number(question: str) -> str:
    text = str(question).strip()
    text = re.sub(r"^\d+、", "", text)
    text = re.sub(r"^\d+\.\s*", "", text)
    return text


def _limit_sentences(text: str, *, max_sentences: int) -> str:
    parts = [part.strip() for part in re.split(r"(?<=[。！？!?])", text) if part.strip()]
    if len(parts) <= max_sentences:
        return text
    return "".join(parts[:max_sentences]).strip()
