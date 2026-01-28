"""
GLM API客户端 - 单例模式
"""
import time
from openai import OpenAI
from config import GLM_CONFIG


class GLMClient:
    _instance = None
    _client = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if self._client is None:
            self._client = OpenAI(
                base_url=GLM_CONFIG["base_url"],
                api_key=GLM_CONFIG["api_key"]
            )

    def chat(self, messages, temperature=0.7, max_retries=3):
        """
        调用GLM聊天接口
        :param messages: 消息列表
        :param temperature: 温度参数
        :param max_retries: 最大重试次数
        :return: 响应内容
        """
        for attempt in range(max_retries):
            try:
                response = self._client.chat.completions.create(
                    model=GLM_CONFIG["model"],
                    messages=messages,
                    temperature=temperature
                )
                return response.choices[0].message.content
            except Exception as e:
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)  # 指数退避
                    continue
                raise e
