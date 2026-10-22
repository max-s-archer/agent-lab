"""Synchronous CLI for one direct model call."""

import argparse
import sys

from agent_lab.config import ConfigurationError, load_settings
from agent_lab.model import ResponseFormatError, TransportError, send_request
from agent_lab.runtime import ToolError, complete_once, run_agent


def build_parser() -> argparse.ArgumentParser:
    """Create the parser for one direct prompt."""

    parser = argparse.ArgumentParser(description="Send one prompt to the configured model.")
    parser.add_argument("prompt", help="The user input to send directly to the model.")
    return parser


def main(argv: list[str] | None = None, model=None, output=None, error_output=None) -> int:
    """Run one bounded agent flow and return a process status code."""

    output = sys.stdout if output is None else output
    error_output = sys.stderr if error_output is None else error_output
    args = build_parser().parse_args(argv)
    try:
        settings = load_settings()
        selected_model = (
            (lambda runtime_settings, messages, trace=None: complete_once(
                runtime_settings, messages, send_request, trace
            ))
            if model is None
            else model
        )
        print(run_agent(settings, args.prompt, selected_model), file=output)
    except (ConfigurationError, TransportError, ResponseFormatError, ToolError) as error:
        print(error, file=error_output)
        return 1
    return 0
