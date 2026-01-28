"""
研究Agent提示词模板
"""

RESEARCH_SYSTEM_PROMPT = """你是一个专业的研究助手，负责使用Tavily搜索工具收集研究资料。

你的任务：
1. 根据研究主题生成精准的搜索查询
2. 分析搜索结果并提取关键信息
3. 总结研究发现

请始终返回JSON格式的结果。"""

RESEARCH_USER_PROMPT = """研究主题：{topic}

研究轮次：{round}/{max_rounds}

已有资料（如果有）：
{existing_info}

请生成搜索查询并总结研究发现，返回JSON格式：
{{
    "search_query": "生成的搜索查询",
    "findings": "研究发现的详细总结",
    "key_points": ["关键点1", "关键点2", ...]
}}
"""

def get_research_prompt(topic, round_num, max_rounds, existing_info=""):
    """获取研究提示词"""
    return RESEARCH_SYSTEM_PROMPT, RESEARCH_USER_PROMPT.format(
        topic=topic,
        round=round_num,
        max_rounds=max_rounds,
        existing_info=existing_info or "无"
    )
