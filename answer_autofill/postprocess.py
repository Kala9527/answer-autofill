from __future__ import annotations

from collections.abc import Sequence

from .prompting import QAItem, TargetItem


LOW_INFO_KEYWORDS = (
    "没什么相关",
    "没有相关",
    "没想法",
    "没有想法",
    "没什么想法",
    "没印象",
    "没有印象",
    "不清楚",
    "不知道",
    "想不起来",
    "不记得",
    "记不清",
)


def repair_answers(
    answers: dict[str, str],
    *,
    valid_answers: Sequence[QAItem],
    group_items: Sequence[QAItem],
    targets: Sequence[TargetItem],
) -> dict[str, str]:
    repaired = {key.upper(): str(value).strip() for key, value in answers.items()}
    if not _has_low_information_context(valid_answers):
        return repaired
    if not _needs_low_information_repair(repaired, targets):
        return repaired

    for target in targets:
        repaired[target.column] = _low_information_answer_for_question(
            target.question,
            group_has_overseas=_group_has_overseas_context(group_items, targets),
        )
    return repaired


def _has_low_information_context(valid_answers: Sequence[QAItem]) -> bool:
    return any(_is_low_information_answer(item.answer) for item in valid_answers)


def _is_low_information_answer(answer: str) -> bool:
    compacted = "".join(str(answer).lower().split())
    return any(keyword in compacted for keyword in LOW_INFO_KEYWORDS)


def _needs_low_information_repair(answers: dict[str, str], targets: Sequence[TargetItem]) -> bool:
    generated = [answers.get(target.column, "").strip() for target in targets]
    if any(not item for item in generated):
        return True
    normalized = {"".join(item.lower().split()) for item in generated}
    return len(normalized) < len(generated)


def _group_has_overseas_context(group_items: Sequence[QAItem], targets: Sequence[TargetItem]) -> bool:
    text = " ".join([item.question for item in group_items] + [target.question for target in targets])
    return "海外" in text


def _low_information_answer_for_question(question: str, *, group_has_overseas: bool) -> str:
    if any(keyword in question for keyword in ("为什么也想", "最吸引")):
        return "我不是因为某个具体人物才强烈想做这件事，更像是把它当作一次短期体验。最吸引我的是公益性、跨文化交流，以及了解医疗体系真实运转的机会。"
    if any(keyword in question for keyword in ("哪个国家", "哪个地区", "哪里")):
        if "海外" in question or group_has_overseas:
            return "暂时没有确定的海外国家或地区。如果只是为了口语题目展开，我会假设去新加坡，因为英语环境较多，医疗体系也比较成熟。"
        return "暂时没有确定的地点。如果只是为了口语题目展开，我会选择一个医疗体系成熟、沟通环境相对友好的地方。"
    if any(keyword in question for keyword in ("为什么", "触动", "原因")):
        return "目前没有某个具体的人真正影响我从事医疗行业，所以这部分只能按假设展开。比较能触动我的，是医疗工作本身和健康、生命责任相关。"
    if any(keyword in question for keyword in ("准备", "人生规划", "影响")):
        return "目前没有正式计划。准备上我会先了解志愿流程、基础急救常识和英语沟通方式；它对人生规划的影响更多是开阔视野，而不是让我转向医疗职业。"
    return "目前没有具体相关经历或明确想法，所以只能按假设展开，保持回答自然但不把它说成真实发生过的事情。"
