"""
编排Agent - 协调研究流程
"""
from agents.research_agent import ResearchAgent
from agents.writer_agent import WriterAgent
from agents.judger_agent import JudgerAgent
from utils.output_manager import OutputManager
from utils.temp_storage import TempStorage
from config import MAX_SEARCH_ROUNDS


class OrchestratorAgent:
    def __init__(self):
        """初始化编排Agent"""
        self.research_agent = ResearchAgent()
        self.writer_agent = WriterAgent()
        self.judger_agent = JudgerAgent()
        self.output_manager = OutputManager()
        self.temp_storage = TempStorage()

    def execute(self, topic, task_id: str = None, verbose: bool = True) -> dict:
        """
        执行研究流程
        :param topic: 研究主题
        :param task_id: 任务ID（可选，自动生成）
        :param verbose: 是否打印日志
        :return: {
            "task_id": "xxx",
            "topic": "xxx",
            "markdown_report": "xxx",
            "report_path": "xxx",
            "steps": [...]  # 所有中间步骤
        }
        """
        # 生成或使用提供的任务ID
        if task_id is None:
            task_id = self.temp_storage.generate_task_id(topic)

        if verbose:
            print(f"\n{'='*60}")
            print(f"开始研究: {topic}")
            print(f"任务ID: {task_id}")
            print(f"{'='*60}\n")

        # 保存初始请求
        self.temp_storage.save_request(
            task_id, 0, "initial",
            {"topic": topic, "task_id": task_id}
        )

        steps = []
        all_findings = []

        # 研究循环
        for round_num in range(1, MAX_SEARCH_ROUNDS + 1):
            if verbose:
                print(f"\n--- 第 {round_num}/{MAX_SEARCH_ROUNDS} 轮研究 ---\n")

            step_num = round_num * 2 - 1

            # 执行研究
            existing_info = "\n\n".join(all_findings) if all_findings else ""

            # 保存研究请求
            research_request = {
                "topic": topic,
                "round_num": round_num,
                "max_rounds": MAX_SEARCH_ROUNDS,
                "existing_info": existing_info
            }
            self.temp_storage.save_request(
                task_id, step_num, "research", research_request
            )

            research_result = self.research_agent.research(
                topic, round_num, MAX_SEARCH_ROUNDS, existing_info
            )

            # 保存研究响应
            self.temp_storage.save_response(
                task_id, step_num, "research", research_result
            )

            # 添加研究发现
            all_findings.append(research_result["findings"])

            # 记录步骤
            steps.append({
                "step": step_num,
                "agent": "research",
                "round": round_num,
                "query": research_result["search_query"],
                "findings": research_result["findings"][:200] + "..." if len(research_result["findings"]) > 200 else research_result["findings"]
            })

            # 评估研究质量
            combined_info = "\n\n".join(all_findings)

            # 保存judger请求
            judger_request = {
                "topic": topic,
                "round_num": round_num,
                "max_rounds": MAX_SEARCH_ROUNDS,
                "research_info": combined_info
            }
            self.temp_storage.save_request(
                task_id, step_num + 1, "judger", judger_request
            )

            judgement = self.judger_agent.judge(
                topic, round_num, MAX_SEARCH_ROUNDS, combined_info
            )

            # 保存judger响应
            self.temp_storage.save_response(
                task_id, step_num + 1, "judger", judgement
            )

            # 记录步骤
            steps.append({
                "step": step_num + 1,
                "agent": "judger",
                "round": round_num,
                "is_sufficient": judgement["is_sufficient"],
                "reason": judgement["reason"]
            })

            # 如果信息充足，退出循环
            if judgement["is_sufficient"]:
                if verbose:
                    print("\n[系统] 研究资料已充足，结束搜索阶段")
                break

            # 如果是最后一轮，也退出
            if round_num >= MAX_SEARCH_ROUNDS:
                if verbose:
                    print(f"\n[系统] 已达到最大搜索轮次({MAX_SEARCH_ROUNDS})，结束搜索阶段")
                break

            if verbose:
                print(f"\n[系统] 继续下一轮研究...")

        # 生成报告
        if verbose:
            print(f"\n{'='*60}")
            print("开始生成研究报告")
            print(f"{'='*60}\n")

        research_data = "\n\n".join(all_findings)

        # 保存writer请求
        writer_step = (MAX_SEARCH_ROUNDS * 2) + 1
        writer_request = {
            "topic": topic,
            "research_data": research_data
        }
        self.temp_storage.save_request(
            task_id, writer_step, "writer", writer_request
        )

        markdown_report = self.writer_agent.write(topic, research_data)

        # 保存writer响应
        self.temp_storage.save_response(
            task_id, writer_step, "writer",
            {"markdown_preview": markdown_report[:500] + "..." if len(markdown_report) > 500 else markdown_report}
        )

        # 保存最终报告
        final_report_path = self.temp_storage.save_final_report(task_id, markdown_report)

        # 保存报告到output目录
        output_path = self.output_manager.save_markdown(markdown_report, topic)

        if verbose:
            print(f"\n{'='*60}")
            print(f"研究完成!")
            print(f"临时文件: {final_report_path}")
            print(f"报告已保存到: {output_path}")
            print(f"{'='*60}\n")

        return {
            "task_id": task_id,
            "topic": topic,
            "markdown_report": markdown_report,
            "report_path": output_path,
            "temp_dir": self.temp_storage.get_task_dir(task_id),
            "steps": steps
        }
