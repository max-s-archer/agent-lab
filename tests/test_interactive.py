from io import StringIO

from agent_lab.cli import main
from agent_lab.config import load_settings
from agent_lab.runtime import MAX_HISTORY_MESSAGES, ToolError, run_turn


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


def test_exit_cancels_the_interactive_run(monkeypatch):
    monkeypatch.setenv("DASHSCOPE_API_KEY", "test-key")
    events = []
    prompts = iter(["exit"])
    status = main(
        ["--interactive"],
        model=lambda *_args: text_response("unused"),
        input_func=lambda _prompt: next(prompts),
        output=StringIO(),
        trace=type("Trace", (), {"append": events.append})(),
    )

    assert status == 0
    assert events == [{"event": "run_finished", "status": "cancelled"}]


def test_quit_and_end_of_input_cancel_the_run(monkeypatch):
    monkeypatch.setenv("DASHSCOPE_API_KEY", "test-key")

    def run(prompts):
        events = []
        status = main(
            ["--interactive"],
            model=lambda *_args: text_response("unused"),
            input_func=prompts,
            output=StringIO(),
            trace=type("Trace", (), {"append": events.append})(),
        )
        return status, events

    quit_status, quit_events = run(lambda _prompt: next(iter(["quit"])))
    end_status, end_events = run(lambda _prompt: None)

    assert quit_status == end_status == 0
    assert quit_events == end_events == [{"event": "run_finished", "status": "cancelled"}]


def test_ctrl_c_cancels_without_a_traceback(monkeypatch):
    monkeypatch.setenv("DASHSCOPE_API_KEY", "test-key")
    events = []
    errors = StringIO()

    def interrupt(_prompt):
        raise KeyboardInterrupt

    status = main(
        ["--interactive"],
        model=lambda *_args: text_response("unused"),
        input_func=interrupt,
        output=StringIO(),
        error_output=errors,
        trace=type("Trace", (), {"append": events.append})(),
    )

    assert status == 130
    assert errors.getvalue() == "Cancelled.\n"
    assert events == [{"event": "run_finished", "status": "cancelled"}]


def test_failed_turn_keeps_the_interactive_session_open(monkeypatch):
    monkeypatch.setenv("DASHSCOPE_API_KEY", "test-key")
    events = []
    prompts = iter(["bad", "exit"])
    errors = StringIO()

    def model(_settings, messages, _trace=None):
        if messages[-1]["content"] == "bad":
            raise ToolError("Unknown tool: missing.")
        return text_response("unused")

    status = main(
        ["--interactive"],
        model=model,
        input_func=lambda _prompt: next(prompts),
        output=StringIO(),
        error_output=errors,
        trace=type("Trace", (), {"append": events.append})(),
    )

    assert status == 0
    assert "Unknown tool: missing." in errors.getvalue()
    assert {"event": "turn_failed", "message": "Unknown tool: missing."} in events
    assert events[-1] == {"event": "run_finished", "status": "cancelled"}
    assert sum(event.get("event") == "run_finished" for event in events) == 1
