"""
测试脚本 - 验证环境配置
"""
import os
from dotenv import load_dotenv
from config import GLM_CONFIG, TAVILY_CONFIG

load_dotenv()

def test_config():
    """测试配置"""
    print("测试配置...")

    # 检查GLM配置
    if not GLM_CONFIG.get("api_key"):
        print("❌ GLM_API_KEY 未配置")
        return False
    print(f"✅ GLM配置: {GLM_CONFIG['model']}")

    # 检查Tavily配置
    if not TAVILY_CONFIG.get("api_key"):
        print("❌ TAVILY_API_KEY 未配置")
        return False
    print(f"✅ Tavily配置: 已配置")

    return True

def test_imports():
    """测试导入"""
    print("\n测试导入...")

    try:
        from utils.llm_client import GLMClient
        print("✅ GLMClient 导入成功")
    except Exception as e:
        print(f"❌ GLMClient 导入失败: {e}")
        return False

    try:
        from agents.research_agent import ResearchAgent
        from agents.writer_agent import WriterAgent
        from agents.judger_agent import JudgerAgent
        print("✅ Agents 导入成功")
    except Exception as e:
        print(f"❌ Agents 导入失败: {e}")
        return False

    return True

def test_directories():
    """测试目录"""
    print("\n测试目录...")

    from utils.output_manager import OutputManager
    manager = OutputManager()
    output_dir = manager.get_output_dir()

    if os.path.exists(output_dir):
        print(f"✅ 输出目录存在: {output_dir}")
    else:
        print(f"❌ 输出目录不存在: {output_dir}")
        return False

    return True

if __name__ == "__main__":
    print("="*50)
    print("Multi-Agent Starter 环境测试")
    print("="*50)

    all_passed = True
    all_passed &= test_config()
    all_passed &= test_imports()
    all_passed &= test_directories()

    print("\n" + "="*50)
    if all_passed:
        print("✅ 所有测试通过! 可以运行 python main.py --topic \"主题\"")
    else:
        print("❌ 部分测试失败，请检查配置")
    print("="*50)
