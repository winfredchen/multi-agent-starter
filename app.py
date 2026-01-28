"""
FastAPI应用入口 - Web界面
"""
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from agents.orchestrator_agent import OrchestratorAgent
import os

# 创建FastAPI应用
app = FastAPI(title="Multi-Agent Starter")

# 获取当前文件所在目录
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 初始化模板引擎
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """首页 - 显示研究表单"""
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/research")
async def research(topic: str = Form(...)):
    """
    执行研究
    :param topic: 研究主题
    :return: 研究结果
    """
    try:
        # 初始化编排Agent
        orchestrator = OrchestratorAgent()

        # 执行研究流程（不打印日志）
        result = orchestrator.execute(topic, verbose=False)

        # 返回结果
        return JSONResponse({
            "success": True,
            "task_id": result["task_id"],
            "topic": result["topic"],
            "markdown_report": result["markdown_report"],
            "report_path": result["report_path"],
            "temp_dir": result["temp_dir"],
            "steps": result["steps"]
        })

    except Exception as e:
        return JSONResponse({
            "success": False,
            "error": str(e)
        }, status_code=500)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
