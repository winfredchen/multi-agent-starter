"""
响应解析器 - 解析LLM返回的JSON/Markdown
"""
import json
import re


class ResponseParser:
    @staticmethod
    def extract_json(content):
        """
        从内容中提取JSON
        :param content: 原始内容
        :return: 解析后的JSON对象
        """
        # 尝试直接解析
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            pass

        # 尝试提取 ```json 代码块
        json_match = re.search(r'```json\s*(.*?)\s*```', content, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group(1))
            except json.JSONDecodeError:
                pass

        # 尝试提取普通代码块
        code_match = re.search(r'```\s*(.*?)\s*```', content, re.DOTALL)
        if code_match:
            try:
                return json.loads(code_match.group(1))
            except json.JSONDecodeError:
                pass

        # 尝试查找JSON对象边界
        obj_match = re.search(r'\{.*\}', content, re.DOTALL)
        if obj_match:
            try:
                return json.loads(obj_match.group(0))
            except json.JSONDecodeError:
                pass

        raise ValueError("无法解析JSON内容")

    @staticmethod
    def extract_markdown(content):
        """
        从内容中提取Markdown
        :param content: 原始内容
        :return: Markdown内容
        """
        # 移除可能的代码块标记
        content = re.sub(r'```markdown\s*', '', content)
        content = re.sub(r'```\s*$', '', content)
        return content.strip()
