"""
ApplicationResearchAgent - 主入口
多Agent协作的应用研究系统
"""
import argparse
from agents.research_agent import ResearchAgent
from agents.writer_agent import WriterAgent
from agents.judger_agent import JudgerAgent
from utils.output_manager import OutputManager
from config import MAX_SEARCH_ROUNDS


def main():
    """主流程控制"""
    parser = argparse.ArgumentParser(description="多Agent协作的应用研究系统")
    parser.add_argument("--topic", type=str, required=True, help="研究主题")
    args = parser.parse_args()

    topic = args.topic
    print(f"\n{'='*60}")
    print(f"开始研究: {topic}")
    print(f"{'='*60}\n")

    # 初始化Agent
    research_agent = ResearchAgent()
    writer_agent = WriterAgent()
    judger_agent = JudgerAgent()
    output_manager = OutputManager()

    # 存储所有研究发现
    all_findings = []

    # 研究循环
    for round_num in range(1, MAX_SEARCH_ROUNDS + 1):
        print(f"\n--- 第 {round_num}/{MAX_SEARCH_ROUNDS} 轮研究 ---\n")

        # 执行研究
        existing_info = "\n\n".join(all_findings) if all_findings else ""
        research_result = research_agent.research(
            topic, round_num, MAX_SEARCH_ROUNDS, existing_info
        )

        # 添加研究发现
        all_findings.append(research_result["findings"])

        # 评估研究质量
        combined_info = "\n\n".join(all_findings)
        judgement = judger_agent.judge(
            topic, round_num, MAX_SEARCH_ROUNDS, combined_info
        )

        # 如果信息充足，退出循环
        if judgement["is_sufficient"]:
            print("\n[系统] 研究资料已充足，结束搜索阶段")
            break

        # 如果是最后一轮，也退出
        if round_num >= MAX_SEARCH_ROUNDS:
            print(f"\n[系统] 已达到最大搜索轮次({MAX_SEARCH_ROUNDS})，结束搜索阶段")
            break

        print(f"\n[系统] 继续下一轮研究...")

    # 生成报告
    print(f"\n{'='*60}")
    print("开始生成研究报告")
    print(f"{'='*60}\n")

    research_data = "\n\n".join(all_findings)
    markdown_report = writer_agent.write(topic, research_data)

    # 保存报告
    filepath = output_manager.save_markdown(markdown_report, topic)

    print(f"\n{'='*60}")
    print(f"研究完成! 报告已保存到: {filepath}")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
