"""
判断Agent - 评估研究资料质量
"""
from utils.llm_client import GLMClient
from utils.response_parser import ResponseParser
from prompts.judger_prompt import get_judger_prompt


class JudgerAgent:
    def __init__(self):
        """初始化判断Agent"""
        self.llm_client = GLMClient()
        self.parser = ResponseParser()

    def judge(self, topic, round_num, max_rounds, research_info):
        """
        评估研究资料是否充足
        :param topic: 研究主题
        :param round_num: 当前轮次
        :param max_rounds: 最大轮次
        :param research_info: 研究资料信息
        :return: 判断结果
        """
        print("[JudgerAgent] 评估研究资料质量...")

        system_prompt, user_prompt = get_judger_prompt(
            topic, round_num, max_rounds, research_info
        )

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]

        response = self.llm_client.chat(messages, temperature=0.3)

        # 解析JSON响应
        result = self.parser.extract_json(response)

        is_sufficient = result.get("is_sufficient", False)
        reason = result.get("reason", "")
        suggested_queries = result.get("suggested_queries", [])

        print(f"[JudgerAgent] 评估结果: {'充足' if is_sufficient else '不充足'}")
        print(f"[JudgerAgent] 理由: {reason}")

        return {
            "is_sufficient": is_sufficient,
            "reason": reason,
            "suggested_queries": suggested_queries
        }
