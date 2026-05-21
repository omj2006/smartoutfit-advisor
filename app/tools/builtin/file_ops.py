from __future__ import annotations

import os

import aiofiles

from app.tools.base import BaseTool, register_tool

WORKSPACE = os.path.join(os.path.dirname(__file__), "..", "..", "..", "workspace")
WORKSPACE = os.path.abspath(WORKSPACE)


def _safe_path(filepath: str) -> str:
    abs_path = os.path.abspath(os.path.join(WORKSPACE, filepath))
    if not abs_path.startswith(WORKSPACE):
        raise ValueError("Access denied: path outside workspace")
    return abs_path


@register_tool
class FileOpsTool(BaseTool):
    name = "file_ops"
    description = "文件操作工具。支持读取、写入、列出文件和创建目录。所有操作限制在workspace目录内。"
    parameters = {
        "type": "object",
        "properties": {
            "action": {
                "type": "string",
                "enum": ["read", "write", "list", "mkdir", "delete"],
                "description": "要执行的操作: read(读取), write(写入), list(列出), mkdir(创建目录), delete(删除)",
            },
            "path": {
                "type": "string",
                "description": "文件或目录路径（相对于workspace）",
            },
            "content": {
                "type": "string",
                "description": "写入文件的内容（仅write操作需要）",
            },
        },
        "required": ["action", "path"],
    }

    async def execute(
        self,
        action: str = "",
        path: str = "",
        content: str = "",
        **kwargs,
    ) -> str:
        try:
            safe_path = _safe_path(path)
        except ValueError as e:
            return str(e)

        if action == "read":
            return await self._read(safe_path)
        elif action == "write":
            return await self._write(safe_path, content)
        elif action == "list":
            return await self._list(safe_path)
        elif action == "mkdir":
            return await self._mkdir(safe_path)
        elif action == "delete":
            return await self._delete(safe_path)
        else:
            return f"未知操作: {action}。支持的操作: read, write, list, mkdir, delete"

    async def _read(self, path: str) -> str:
        if not os.path.exists(path):
            return f"文件不存在: {path}"
        async with aiofiles.open(path, "r", encoding="utf-8") as f:
            content = await f.read()
        return content

    async def _write(self, path: str, content: str) -> str:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        async with aiofiles.open(path, "w", encoding="utf-8") as f:
            await f.write(content)
        return f"文件写入成功: {path}"

    async def _list(self, path: str) -> str:
        if not os.path.exists(path):
            return f"目录不存在: {path}"
        if not os.path.isdir(path):
            return f"不是目录: {path}"
        items = os.listdir(path)
        if not items:
            return "目录为空"
        result = []
        for item in sorted(items):
            full_path = os.path.join(path, item)
            item_type = "📁" if os.path.isdir(full_path) else "📄"
            result.append(f"{item_type} {item}")
        return "\n".join(result)

    async def _mkdir(self, path: str) -> str:
        os.makedirs(path, exist_ok=True)
        return f"目录创建成功: {path}"

    async def _delete(self, path: str) -> str:
        if not os.path.exists(path):
            return f"文件不存在: {path}"
        os.remove(path)
        return f"文件删除成功: {path}"
