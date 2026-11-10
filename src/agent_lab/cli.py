"""Synchronous CLI for one-shot and local interactive sessions."""

import argparse
import sys
from pathlib import Path

from agent_lab.config import ConfigurationError, load_settings
from agent_lab.model import ResponseFormatError, TransportError, send_request
from agent_lab.runtime import MAX_HISTORY_MESSAGES, ToolError, complete_once, run_turn
from agent_lab.trace import JsonlTrace

EXIT_COMMANDS = {"exit", "quit"}


def build_parser() -> argparse.ArgumentParser:
    """Create the parser for one direct prompt."""

    parser = argparse.ArgumentParser(description="Send one prompt to the configured model.")
    parser.add_argument("prompt", nargs="?", help="The user input to send directly to the model.")
    parser.add_argument("--interactive", action="store_true", help="Keep one local conversation open.")
    return parser


def selected_model(model):
    """Return the injected model or the real one-request transport."""

    if model is not None:
        return model
    return lambda runtime_settings, messages, trace=None: complete_once(
        runtime_settings, messages, send_request, trace
    )


def run_interactive(settings, model, input_func, output, error_output, trace) -> int:
    """Read prompts until exit and resend only this process's history."""

    messages = []
    while True:
        prompt = input_func("agent-lab> ")
        if prompt is None or prompt.strip().casefold() in EXIT_COMMANDS:
            trace.append({"event": "run_finished", "status": "completed"})
            return 0
        if not prompt.strip():
            continue
        try:
            answer, messages = run_turn(settings, messages, prompt, model, trace)
        except (TransportError, ResponseFormatError, ToolError) as error:
            trace.append({"event": "run_finished", "status": "error", "message": str(error)})
            print(error, file=error_output)
            continue
        messages = messages[-MAX_HISTORY_MESSAGES:]
        print(answer, file=output)


def main(
    argv: list[str] | None = None,
    model=None,
    input_func=None,
    output=None,
    error_output=None,
    trace=None,
) -> int:
    """Run one bounded agent flow and return a process status code."""

    output = sys.stdout if output is None else output
    error_output = sys.stderr if error_output is None else error_output
    args = build_parser().parse_args(argv)
    try:
        settings = load_settings()
        active_trace = trace or JsonlTrace(Path("traces"), settings.api_key)
        active_model = selected_model(model)
        if args.interactive:
            return run_interactive(
                settings,
                active_model,
                input if input_func is None else input_func,
                output,
                error_output,
                active_trace,
            )
        if args.prompt is None:
            raise ConfigurationError("Provide a prompt or use --interactive.")
        print(run_turn(settings, [], args.prompt, active_model, active_trace)[0], file=output)
        active_trace.append({"event": "run_finished", "status": "completed"})
    except (ConfigurationError, TransportError, ResponseFormatError, ToolError) as error:
        if "active_trace" in locals():
            active_trace.append({"event": "run_finished", "status": "error", "message": str(error)})
        print(error, file=error_output)
        return 1
    return 0
