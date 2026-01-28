"""
输出管理器 - 管理Markdown文件输出
"""
import os
from datetime import datetime
from config import MARKDOWN_DIR


class OutputManager:
    def __init__(self):
        """初始化输出管理器，确保输出目录存在"""
        if not os.path.exists(MARKDOWN_DIR):
            os.makedirs(MARKDOWN_DIR)

    def save_markdown(self, content, topic):
        """
        保存Markdown文件
        :param content: Markdown内容
        :param topic: 研究主题
        :return: 保存的文件路径
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        # 清理主题名称，移除不合法字符
        safe_topic = "".join(c for c in topic if c.isalnum() or c in (' ', '-', '_')).strip()
        safe_topic = safe_topic[:50]  # 限制长度
        filename = f"{safe_topic}_{timestamp}.md"
        filepath = os.path.join(MARKDOWN_DIR, filename)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        return filepath

    def get_output_dir(self):
        """获取输出目录路径"""
        return MARKDOWN_DIR
