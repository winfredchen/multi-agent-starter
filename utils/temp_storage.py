"""
临时存储管理器 - 管理temp目录和中间步骤数据
"""
import os
import json
from datetime import datetime
from config import TEMP_DIR


class TempStorage:
    def __init__(self):
        """初始化临时存储管理器，确保temp目录存在"""
        if not os.path.exists(TEMP_DIR):
            os.makedirs(TEMP_DIR)

    def create_task_dir(self, task_id: str) -> str:
        """
        为任务创建子目录
        :param task_id: 任务ID
        :return: 任务目录路径
        """
        task_dir = os.path.join(TEMP_DIR, task_id)
        if not os.path.exists(task_dir):
            os.makedirs(task_dir)
        return task_dir

    def save_request(self, task_id: str, step: int, agent: str, data: dict):
        """
        保存请求到临时目录
        :param task_id: 任务ID
        :param step: 步骤编号
        :param agent: Agent名称
        :param data: 请求数据
        """
        task_dir = self.create_task_dir(task_id)
        filename = f"{step:02d}_{agent}_request.json"
        filepath = os.path.join(task_dir, filename)

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def save_response(self, task_id: str, step: int, agent: str, data: dict):
        """
        保存响应到临时目录
        :param task_id: 任务ID
        :param step: 步骤编号
        :param agent: Agent名称
        :param data: 响应数据
        """
        task_dir = self.create_task_dir(task_id)
        filename = f"{step:02d}_{agent}_response.json"
        filepath = os.path.join(task_dir, filename)

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def save_final_report(self, task_id: str, markdown_content: str) -> str:
        """
        保存最终报告到临时目录
        :param task_id: 任务ID
        :param markdown_content: Markdown内容
        :return: 文件路径
        """
        task_dir = self.create_task_dir(task_id)
        filepath = os.path.join(task_dir, "final_report.md")

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(markdown_content)

        return filepath

    def get_task_dir(self, task_id: str) -> str:
        """
        获取任务目录路径
        :param task_id: 任务ID
        :return: 任务目录路径
        """
        return os.path.join(TEMP_DIR, task_id)

    def generate_task_id(self, topic: str) -> str:
        """
        根据主题生成任务ID
        :param topic: 研究主题
        :return: 任务ID
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        # 清理主题名称
        safe_topic = "".join(c for c in topic if c.isalnum() or c in (' ', '-', '_')).strip()
        safe_topic = safe_topic.replace(' ', '_')[:30]
        return f"{safe_topic}_{timestamp}"
