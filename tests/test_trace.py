import json
from io import StringIO

from agent_lab.cli import main


def text_response(content):
    return {"choices": [{"message": {"content": content}}]}


def read_events(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def test_trace_redacts_secret_and_records_completion(tmp_path, monkeypatch):
    monkeypatch.setenv("DASHSCOPE_API_KEY", "secret-value")
    monkeypatch.chdir(tmp_path)

    def model(_settings, messages, trace=None):
        trace.append({"direction": "request", "body": {"headers": {"Authorization": "Bearer secret-value"}}})
        return text_response("ok")

    status = main(["hello"], model=model, output=StringIO(), error_output=StringIO())

    assert status == 0
    events = read_events(next(tmp_path.joinpath("traces").glob("*.jsonl")))
    rendered = json.dumps(events)
    assert "secret-value" not in rendered
    assert events[-1]["event"] == "run_finished"
    assert events[-1]["status"] == "completed"


def test_trace_records_errors(tmp_path, monkeypatch):
    monkeypatch.setenv("DASHSCOPE_API_KEY", "secret-value")
    monkeypatch.chdir(tmp_path)

    status = main(
        ["hello"],
        model=lambda _settings, _messages, _trace: {},
        output=StringIO(),
        error_output=StringIO(),
    )

    assert status == 1
    events = read_events(next(tmp_path.joinpath("traces").glob("*.jsonl")))
    assert events[-1]["status"] == "error"
