"""
配置文件 - API密钥和路径配置
"""
import os
from dotenv import load_dotenv

load_dotenv()

# GLM API配置
GLM_CONFIG = {
    "base_url": os.getenv("BASE_URL", "https://open.bigmodel.cn/api/paas/v4/"),
    "api_key": os.getenv("API_KEY"),
    "model": os.getenv("MODEL", "glm-4-flash")
}

# Tavily API配置
TAVILY_CONFIG = {
    "api_key": os.getenv("TAVILY_API_KEY")
}

# 输出路径配置
OUTPUT_DIR = os.path.join(os.getcwd(), "output")
MARKDOWN_DIR = os.path.join(OUTPUT_DIR, "markdown")

# 临时存储路径配置
TEMP_DIR = os.path.join(os.getcwd(), "temp")

# 最大搜索轮次
MAX_SEARCH_ROUNDS = 3
