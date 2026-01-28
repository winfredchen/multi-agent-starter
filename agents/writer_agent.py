"""
写作Agent - 生成Markdown报告
"""
from utils.llm_client import GLMClient
from utils.response_parser import ResponseParser
from prompts.writer_prompt import get_writer_prompt


class WriterAgent:
    def __init__(self):
        """初始化写作Agent"""
        self.llm_client = GLMClient()
        self.parser = ResponseParser()

    def write(self, topic, research_data):
        """
        生成研究报告
        :param topic: 研究主题
        :param research_data: 研究资料
        :return: Markdown报告
        """
        print("[WriterAgent] 开始生成研究报告...")

        system_prompt, user_prompt = get_writer_prompt(topic, research_data)

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]

        response = self.llm_client.chat(messages, temperature=0.7)

        # 提取Markdown内容
        markdown_content = self.parser.extract_markdown(response)

        print("[WriterAgent] 报告生成完成")
        return markdown_content
