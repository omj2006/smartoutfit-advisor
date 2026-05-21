from __future__ import annotations

import math
import operator

from app.tools.base import BaseTool, register_tool

SAFE_OPERATORS = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.truediv,
    "**": operator.pow,
    "%": operator.mod,
    "//": operator.floordiv,
}

SAFE_FUNCTIONS = {
    "abs": abs,
    "round": round,
    "min": min,
    "max": max,
    "sum": sum,
    "sqrt": math.sqrt,
    "log": math.log,
    "log10": math.log10,
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "pi": math.pi,
    "e": math.e,
    "ceil": math.ceil,
    "floor": math.floor,
}


@register_tool
class CalculatorTool(BaseTool):
    name = "calculator"
    description = "执行数学计算。支持基本运算（加减乘除）和数学函数（sin, cos, sqrt, log等）。"
    parameters = {
        "type": "object",
        "properties": {
            "expression": {
                "type": "string",
                "description": "要计算的数学表达式，例如 '2 + 3 * 4' 或 'sqrt(16)'",
            }
        },
        "required": ["expression"],
    }

    async def execute(self, expression: str = "", **kwargs) -> str:
        allowed_names = {k: v for k, v in SAFE_FUNCTIONS.items()}
        try:
            result = eval(expression, {"__builtins__": {}}, allowed_names)
            return f"{expression} = {result}"
        except Exception as e:
            return f"计算错误: {str(e)}"
