import json
import urllib.error
from io import StringIO

import pytest

from agent_lab.cli import main
from agent_lab.config import (
    BASE_URL,
    CREDENTIAL_VARIABLE,
    MODEL_NAME,
    TIMEOUT_SECONDS,
    load_settings,
)
from agent_lab.model import (
    ResponseFormatError,
    TransportError,
    build_request,
    extract_text,
    run_once,
    send_request,
)


def test_request_uses_cli_input_and_confirmed_configuration():
    settings = load_settings(api_key="test-key")

    request = build_request(settings, "Hello")

    assert request["method"] == "POST"
    assert request["url"] == f"{BASE_URL}/chat/completions"
    assert request["timeout_seconds"] == TIMEOUT_SECONDS
    assert request["json"] == {
        "model": MODEL_NAME,
        "messages": [{"role": "user", "content": "Hello"}],
    }
    assert request["headers"]["Authorization"] == "Bearer test-key"


def test_successful_simulated_response_is_returned_directly():
    settings = load_settings(api_key="test-key")

    def transport(request):
        assert request["json"]["messages"][0]["content"] == "Hello"
        return {"choices": [{"message": {"content": "Simulated reply"}}]}

    assert run_once(settings, "Hello", transport) == "Simulated reply"


def test_missing_configuration_is_reported_without_network(monkeypatch):
    monkeypatch.delenv(CREDENTIAL_VARIABLE, raising=False)
    error_output = StringIO()

    status = main(["Hello"], error_output=error_output)

    assert status == 1
    assert error_output.getvalue().strip() == f"Missing required environment variable: {CREDENTIAL_VARIABLE}"


def test_transport_failure_is_distinct(monkeypatch):
    monkeypatch.setenv(CREDENTIAL_VARIABLE, "test-key")
    error_output = StringIO()

    def transport(_request):
        raise TransportError("Model request failed.")

    status = main(["Hello"], transport=transport, error_output=error_output)

    assert status == 1
    assert error_output.getvalue().strip() == "Model request failed."


def test_malformed_response_is_distinct(monkeypatch):
    monkeypatch.setenv(CREDENTIAL_VARIABLE, "test-key")
    error_output = StringIO()

    status = main(["Hello"], transport=lambda _request: {}, error_output=error_output)

    assert status == 1
    assert error_output.getvalue().strip() == "Model response does not contain text content."


def test_cli_displays_simulated_text_without_credentials(monkeypatch):
    monkeypatch.setenv(CREDENTIAL_VARIABLE, "test-key")
    output = StringIO()

    status = main(
        ["Hello"],
        transport=lambda _request: {"choices": [{"message": {"content": "Simulated reply"}}]},
        output=output,
    )

    displayed = output.getvalue()
    assert status == 0
    assert displayed.strip() == "Simulated reply"
    assert "test-key" not in displayed


def test_extract_text_rejects_malformed_response():
    with pytest.raises(ResponseFormatError):
        extract_text({"choices": []})


def test_http_transport_reads_simulated_success(monkeypatch):
    request = build_request(load_settings(api_key="test-key"), "Hello")

    class Response:
        def read(self):
            return json.dumps({"choices": [{"message": {"content": "HTTP reply"}}]}).encode()

        def __enter__(self):
            return self

        def __exit__(self, *_args):
            return None

    def urlopen(outgoing, timeout):
        assert outgoing.full_url == request["url"]
        assert timeout == TIMEOUT_SECONDS
        assert "test-key" not in outgoing.full_url
        return Response()

    monkeypatch.setattr("agent_lab.model.urllib.request.urlopen", urlopen)

    assert send_request(request)["choices"][0]["message"]["content"] == "HTTP reply"


def test_http_transport_reports_timeout(monkeypatch):
    def urlopen(_outgoing, timeout):
        raise TimeoutError

    monkeypatch.setattr("agent_lab.model.urllib.request.urlopen", urlopen)

    with pytest.raises(TransportError, match="Model request failed\\.$"):
        send_request(build_request(load_settings(api_key="test-key"), "Hello"))


def test_http_transport_reports_status_without_credential(monkeypatch):
    def urlopen(_outgoing, timeout):
        raise urllib.error.HTTPError("https://example.test", 401, "Unauthorized", {}, None)

    monkeypatch.setattr("agent_lab.model.urllib.request.urlopen", urlopen)

    with pytest.raises(TransportError, match="HTTP 401\\.$") as error:
        send_request(build_request(load_settings(api_key="test-key"), "Hello"))
    assert "test-key" not in str(error.value)
