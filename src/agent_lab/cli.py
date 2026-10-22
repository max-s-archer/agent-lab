"""Synchronous CLI for one direct model call."""

import argparse
import sys

from agent_lab.config import ConfigurationError, load_settings
from agent_lab.model import ResponseFormatError, TransportError, run_once, send_request


def build_parser() -> argparse.ArgumentParser:
    """Create the parser for one direct prompt."""

    parser = argparse.ArgumentParser(description="Send one prompt to the configured model.")
    parser.add_argument("prompt", help="The user input to send directly to the model.")
    return parser


def main(argv: list[str] | None = None, transport=None, output=None, error_output=None) -> int:
    """Run one direct model call and return a process status code."""

    output = sys.stdout if output is None else output
    error_output = sys.stderr if error_output is None else error_output
    args = build_parser().parse_args(argv)
    try:
        settings = load_settings()
        selected_transport = send_request if transport is None else transport
        print(run_once(settings, args.prompt, selected_transport), file=output)
    except (ConfigurationError, TransportError, ResponseFormatError) as error:
        print(error, file=error_output)
        return 1
    return 0
