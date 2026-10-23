"""Bounded runtime for one direct answer or one calculation."""

import json
from collections.abc import Mapping
from decimal import Decimal, InvalidOperation

from agent_lab.model import ResponseFormatError, extract_decision

CALCULATE_TOOL = {
    "type": "function",
    "function": {
        "name": "calculate",
        "description": "Perform one deterministic arithmetic operation.",
        "parameters": {
            "type": "object",
            "properties": {
                "operation": {
                    "type": "string",
                    "enum": ["add", "subtract", "multiply", "divide"],
                },
                "left": {"type": "number"},
                "right": {"type": "number"},
            },
            "required": ["operation", "left", "right"],
            "additionalProperties": False,
        },
    },
}
LIST_FILES_TOOL = {
    "type": "function",
    "function": {
        "name": "list_workspace_files",
        "description": "List at most 20 file names inside the configured workspace.",
        "parameters": {
            "type": "object",
            "properties": {"relative_directory": {"type": "string"}},
            "required": ["relative_directory"],
            "additionalProperties": False,
        },
    },
}
MAX_MODEL_CALLS = 2
OPERATIONS = {
    "add": lambda left, right: left + right,
    "subtract": lambda left, right: left - right,
    "multiply": lambda left, right: left * right,
    "divide": lambda left, right: left / right,
}


class ToolError(Exception):
    """Raised when a model requests a tool that cannot be executed."""


def calculate(arguments: Mapping[str, object]) -> str:
    """Execute one explicit arithmetic operation without evaluating text."""

    try:
        operation = arguments["operation"]
        left = Decimal(str(arguments["left"]))
        right = Decimal(str(arguments["right"]))
        if not isinstance(operation, str) or operation not in OPERATIONS:
            raise ToolError("Unknown calculate operation.")
        if operation == "divide" and right == 0:
            raise ToolError("Division by zero is not allowed.")
        return str(OPERATIONS[operation](left, right))
    except (KeyError, InvalidOperation, ValueError) as error:
        raise ToolError("Invalid calculate arguments.") from error


def execute_tool(tool_request: dict) -> str:
    """Execute one registered tool after validating its name."""

    from agent_lab.files import list_workspace_files

    tools = {"calculate": calculate, "list_workspace_files": list_workspace_files}
    name = tool_request["name"]
    if name not in tools:
        raise ToolError(f"Unknown tool: {name}.")
    return tools[name](tool_request["arguments"])


def run_agent(settings, user_input: str, model, trace=None) -> str:
    """Run at most two model decisions and one validated tool call."""

    messages: list[dict] = [{"role": "user", "content": user_input}]
    for _ in range(MAX_MODEL_CALLS):
        response = model(settings, messages, trace)
        text, tool_request = extract_decision(response)
        if text is not None:
            return text
        if tool_request["name"] not in {"calculate", "list_workspace_files"}:
            raise ToolError(f"Unknown tool: {tool_request['name']}.")
        result = execute_tool(tool_request)
        messages.append(
            {
                "role": "assistant",
                "tool_calls": [
                    {
                        "id": tool_request["id"],
                        "type": "function",
                        "function": {
                            "name": tool_request["name"],
                            "arguments": json.dumps(tool_request["arguments"]),
                        },
                    }
                ],
            }
        )
        messages.append(
            {
                "role": "tool",
                "tool_call_id": tool_request["id"],
                "content": result,
            }
        )
        if trace is not None:
            trace.append({"direction": "local-tool", "name": tool_request["name"], "result": result})
    raise ResponseFormatError("Model call limit reached.")


def complete_once(settings, messages, transport, trace=None):
    """Adapt the existing single-call transport to the runtime model boundary."""

    payload = {
        "model": settings.model,
        "messages": messages,
        "tools": [CALCULATE_TOOL, LIST_FILES_TOOL],
        "tool_choice": "auto",
    }
    if trace is not None:
        trace.append({"direction": "request", "body": payload})
    response = transport(
        {
            "method": "POST",
            "url": f"{settings.base_url}/chat/completions",
            "timeout_seconds": settings.timeout_seconds,
            "headers": {
                "Authorization": f"Bearer {settings.api_key}",
                "Content-Type": "application/json",
            },
            "json": payload,
        }
    )
    if trace is not None:
        trace.append({"direction": "response", "body": response})
    return response
