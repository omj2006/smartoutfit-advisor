from __future__ import annotations

import asyncio
import sys
from io import StringIO

from app.tools.base import BaseTool, register_tool


@register_tool
class CodeRunnerTool(BaseTool):
    name = "code_runner"
    description = "执行Python代码并返回输出结果。代码在沙盒环境中运行。"
    parameters = {
        "type": "object",
        "properties": {
            "code": {
                "type": "string",
                "description": "要执行的Python代码",
            },
            "timeout": {
                "type": "integer",
                "description": "超时时间（秒），默认30",
                "default": 30,
            },
        },
        "required": ["code"],
    }

    async def execute(self, code: str = "", timeout: int = 30, **kwargs) -> str:
        try:
            result = await asyncio.wait_for(
                asyncio.to_thread(self._run_code, code),
                timeout=timeout,
            )
            return result
        except asyncio.TimeoutError:
            return f"代码执行超时（{timeout}秒）"
        except Exception as e:
            return f"代码执行错误: {str(e)}"

    def _run_code(self, code: str) -> str:
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        sys.stdout = StringIO()
        sys.stderr = StringIO()

        sandbox_globals = {
            "__builtins__": __builtins__,
        }

        try:
            exec(code, sandbox_globals)
            output = sys.stdout.getvalue()
            error_output = sys.stderr.getvalue()

            result_parts = []
            if output:
                result_parts.append(f"输出:\n{output}")
            if error_output:
                result_parts.append(f"错误:\n{error_output}")
            if not result_parts:
                result_parts.append("代码执行成功（无输出）")

            return "\n".join(result_parts)
        except Exception as e:
            return f"执行错误: {type(e).__name__}: {str(e)}"
        finally:
            sys.stdout = old_stdout
            sys.stderr = old_stderr
