"""
判断Agent提示词模板
"""

JUDGER_SYSTEM_PROMPT = """你是一个研究质量评估专家，负责判断研究资料是否充足。

评估标准：
1. 信息覆盖面是否全面
2. 关键问题是否都有答案
3. 是否有足够的具体细节和数据支持

请始终返回JSON格式的判断结果。"""

JUDGER_USER_PROMPT = """研究主题：{topic}

当前研究轮次：{round}/{max_rounds}

已收集的研究资料：
{research_info}

请评估研究资料是否充足，返回JSON格式：
{{
    "is_sufficient": true/false,
    "reason": "判断理由",
    "suggested_queries": ["建议搜索的主题1", "建议搜索的主题2", ...]
}}
"""

def get_judger_prompt(topic, round_num, max_rounds, research_info):
    """获取判断提示词"""
    return JUDGER_SYSTEM_PROMPT, JUDGER_USER_PROMPT.format(
        topic=topic,
        round=round_num,
        max_rounds=max_rounds,
        research_info=research_info
    )
