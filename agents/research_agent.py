"""
研究Agent - 使用Tavily进行网络搜索
"""
from tavily import TavilyClient
from utils.llm_client import GLMClient
from utils.response_parser import ResponseParser
from prompts.research_prompt import get_research_prompt
from config import TAVILY_CONFIG


class ResearchAgent:
    def __init__(self):
        """初始化研究Agent"""
        self.llm_client = GLMClient()
        self.tavily_client = TavilyClient(api_key=TAVILY_CONFIG["api_key"])
        self.parser = ResponseParser()

    def research(self, topic, round_num, max_rounds, existing_info=""):
        """
        执行研究
        :param topic: 研究主题
        :param round_num: 当前轮次
        :param max_rounds: 最大轮次
        :param existing_info: 已有信息
        :return: 研究结果
        """
        print(f"[ResearchAgent] 开始第 {round_num}/{max_rounds} 轮研究...")

        # 生成搜索查询
        system_prompt, user_prompt = get_research_prompt(
            topic, round_num, max_rounds, existing_info
        )

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]

        response = self.llm_client.chat(messages, temperature=0.5)

        # 解析响应获取搜索查询
        try:
            result = self.parser.extract_json(response)
            search_query = result.get("search_query", topic)
        except:
            search_query = topic

        # 执行Tavily搜索
        print(f"[ResearchAgent] 搜索查询: {search_query}")
        search_results = self._tavily_search(search_query)

        # 总结搜索结果
        findings = self._summarize_findings(search_query, search_results)

        return {
            "search_query": search_query,
            "findings": findings,
            "raw_results": search_results
        }

    def _tavily_search(self, query):
        """
        使用Tavily进行搜索
        :param query: 搜索查询
        :return: 搜索结果
        """
        try:
            response = self.tavily_client.search(
                query=query,
                search_depth="advanced",
                max_results=10,
                include_images=False,
                include_answer=True
            )
            return response
        except Exception as e:
            print(f"[ResearchAgent] 搜索出错: {e}")
            return {"answer": "", "results": []}

    def _summarize_findings(self, query, search_results):
        """
        总结搜索结果
        :param query: 搜索查询
        :param search_results: 搜索结果
        :return: 总结内容
        """
        summary_parts = [f"## 搜索查询: {query}\n"]

        # 添加Tavily的AI答案
        if search_results.get("answer"):
            summary_parts.append(f"**AI摘要**: {search_results['answer']}\n")

        # 添加搜索结果
        results = search_results.get("results", [])
        if results:
            summary_parts.append("**搜索结果**:\n")
            for i, result in enumerate(results[:5], 1):
                title = result.get("title", "无标题")
                url = result.get("url", "")
                content = result.get("content", "")[:300]
                summary_parts.append(
                    f"{i}. **{title}**\n"
                    f"   - 链接: {url}\n"
                    f"   - 内容: {content}...\n"
                )

        return "\n".join(summary_parts)
