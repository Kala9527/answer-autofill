from __future__ import annotations

import asyncio

from .config import ModelConfig
from .invalid import is_invalid_answer
from .prompting import QAItem, TargetItem, build_cell_messages, clean_plain_answer


class AnswerLLMClient:
    def __init__(self, config: ModelConfig, *, max_concurrency: int = 8) -> None:
        try:
            from openai import AsyncOpenAI
        except ImportError as exc:
            raise RuntimeError("Missing openai package. Run setup_env first.") from exc

        self._config = config
        self._client = AsyncOpenAI(
            base_url=config.base_url,
            api_key=config.api_key,
            timeout=config.timeout_seconds,
            max_retries=0,
        )
        self._semaphore = asyncio.Semaphore(max(1, max_concurrency))

    async def complete_cell(
        self,
        *,
        basic_info: list[QAItem],
        group_items: list[QAItem],
        context_answers: list[QAItem],
        target: TargetItem,
    ) -> str:
        messages = build_cell_messages(
            basic_info=basic_info,
            group_items=group_items,
            context_answers=context_answers,
            target=target,
        )
        last_error: Exception | None = None
        for _ in range(self._config.retries):
            try:
                async with self._semaphore:
                    response = await self._client.chat.completions.create(
                        model=self._config.model,
                        messages=messages,
                        temperature=self._config.temperature,
                        max_tokens=min(self._config.max_tokens, 180),
                        stop=["\n", "基础信息", "同组题目", "同组参考", "要回答的问题"],
                    )
                answer = clean_plain_answer(response.choices[0].message.content)
                if not answer or is_invalid_answer(answer) or _looks_like_question_echo(answer, target):
                    raise ValueError("model returned empty or invalid plain answer")
                return answer
            except Exception as exc:  # noqa: BLE001 - preserve final model/client error for reporting.
                last_error = exc
        assert last_error is not None
        raise last_error

    async def aclose(self) -> None:
        await self._client.close()


def _looks_like_question_echo(answer: str, target: TargetItem) -> bool:
    compact_answer = "".join(answer.split())
    compact_question = "".join(target.question.split())
    if target.column in answer:
        return True
    if compact_question and compact_question[:10] in compact_answer:
        return True
    forbidden = (
        "上一次输出",
        "格式不符合要求",
        "请只输出",
        "不要JSON",
        "不要Markdown",
        "任务：补全",
        "输出规则",
        "直接给出答案正文",
        "他/她为什么想从事医疗行业",
        "需要补全的问题",
    )
    return any(item in answer for item in forbidden)
