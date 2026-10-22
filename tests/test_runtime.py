import pytest

from agent_lab.config import load_settings
from agent_lab.model import ResponseFormatError
from agent_lab.runtime import ToolError, calculate, run_agent


def text_response(content):
    return {"choices": [{"message": {"content": content}}]}


def tool_response(name, arguments):
    return {
        "choices": [
            {"message": {"tool_calls": [{"function": {"name": name, "arguments": arguments}}]}}
        ]
    }


def test_direct_answer_does_not_execute_tool():
    calls = {"count": 0}

    def model(_settings, _messages):
        calls["count"] += 1
        return text_response("Direct answer")

    assert run_agent(load_settings(api_key="test-key"), "Hello", model) == "Direct answer"
    assert calls["count"] == 1


def test_calculate_result_is_returned_to_model():
    seen = []

    def model(_settings, messages):
        seen.append(messages[-1])
        if len(seen) == 1:
            return tool_response("calculate", {"operation": "add", "left": 2, "right": 3})
        return text_response("The result is 5")

    assert run_agent(load_settings(api_key="test-key"), "Add 2 and 3", model) == "The result is 5"
    assert seen[1] == {"role": "tool", "name": "calculate", "content": "5"}


def test_unknown_tool_is_rejected():
    def model(_settings, _messages):
        return tool_response("shell", {})

    with pytest.raises(ToolError, match="Unknown tool: shell\\."):
        run_agent(load_settings(api_key="test-key"), "Run", model)


def test_invalid_calculate_arguments_are_rejected():
    with pytest.raises(ToolError, match="Invalid calculate arguments\\."):
        calculate({"operation": "add", "left": "two", "right": 1})


def test_model_call_limit_stops_second_tool_request():
    def model(_settings, _messages):
        return tool_response("calculate", {"operation": "add", "left": 1, "right": 1})

    with pytest.raises(ResponseFormatError, match="Model call limit reached\\."):
        run_agent(load_settings(api_key="test-key"), "Loop", model)
