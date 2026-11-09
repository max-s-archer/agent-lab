from io import StringIO

from agent_lab.cli import main
from agent_lab.config import load_settings
from agent_lab.runtime import MAX_HISTORY_MESSAGES, run_turn


def text_response(content):
    return {"choices": [{"message": {"content": content}}]}


def test_interactive_session_resends_local_history(monkeypatch):
    monkeypatch.setenv("DASHSCOPE_API_KEY", "test-key")
    seen = []

    def model(_settings, messages, _trace=None):
        seen.append([item["content"] for item in messages if "content" in item])
        return text_response(f"reply {len(seen)}")

    prompts = iter(["first", "second", "exit"])
    output = StringIO()
    status = main(
        ["--interactive"],
        model=model,
        input_func=lambda _prompt: next(prompts),
        output=output,
    )

    assert status == 0
    assert seen[0] == ["first"]
    assert seen[1] == ["first", "reply 1", "second"]
    assert output.getvalue().splitlines() == ["reply 1", "reply 2"]


def test_history_is_limited_to_eight_messages():
    history = [{"role": "user", "content": str(index)} for index in range(MAX_HISTORY_MESSAGES)]

    def model(_settings, messages, _trace=None):
        assert len(messages) == MAX_HISTORY_MESSAGES + 1
        return text_response("latest")

    _answer, updated = run_turn(load_settings(api_key="test-key"), history, "new", model)

    assert len(updated) == MAX_HISTORY_MESSAGES + 2
    assert updated[-2:] == [
        {"role": "user", "content": "new"},
        {"role": "assistant", "content": "latest"},
    ]
