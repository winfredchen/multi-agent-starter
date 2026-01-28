"""
Multi-Agent Starter - 主入口
多Agent协作系统的快速入门参考项目
"""
import argparse
from agents.orchestrator_agent import OrchestratorAgent


def main():
    """主流程控制"""
    parser = argparse.ArgumentParser(description="多Agent协作的应用研究系统")
    parser.add_argument("--topic", type=str, required=True, help="研究主题")
    args = parser.parse_args()

    topic = args.topic

    # 初始化编排Agent
    orchestrator = OrchestratorAgent()

    # 执行研究流程
    result = orchestrator.execute(topic)

    print(f"\n研究完成! 报告已保存到: {result['report_path']}")
    print(f"临时文件目录: {result['temp_dir']}\n")


if __name__ == "__main__":
    main()
