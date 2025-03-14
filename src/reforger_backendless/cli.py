"""Command line entrypoint for reforger-backendless"""

import argparse
import enum
import logging
import os
import sys

from reforger_backendless.backendless_server import (
    PROFILE_DIR,
    REFORGER_DIR,
    BackendlessServer,
)


class Exit(enum.IntEnum):
    """Exit codes for the program"""

    SUCCESS = 0
    FAILURE = 1


def parse_arguments(args: list[str]) -> argparse.Namespace:
    """Parse generic arguments, given as parameters

    This function can be used programatically to emulate CLI calls, either
    during tests or via other interfaces like API calls.


    Arguments:
      args: The arguments to parse, usually from `sys.argv` array.

    """
    parser = argparse.ArgumentParser(
        "reforger-backendless",
        description=(
            "A set of helper scripts to run an Arma Reforger server "
            "without the BI backend"
        ),
    )
    parser.set_defaults(func=lambda _: parser.print_help(sys.stderr))

    subparsers = parser.add_subparsers()
    run = subparsers.add_parser("run", help="Run the server")
    run.set_defaults(func=_run)
    run.add_argument(
        "--config",
        "-c",
        help="Path to the configuration file",
        default="config.json",
    )
    run.add_argument(
        "--podman",
        "-p",
        help="Use podman to run the server",
        action="store_true",
    )
    run.add_argument(
        "--dry-run",
        "-n",
        help="Print the command to run without executing it",
        action="store_true",
    )
    run.add_argument(
        "--host-network",
        "-H",
        help="Use the host network for podman",
        action="store_true",
    )
    run.add_argument(
        "--extra-args", "-e", help="Extra arguments to pass to the server", default=""
    )
    run.add_argument(
        "--reforger-dir",
        help="Path to the reforger installation directory",
        default=REFORGER_DIR,
    )
    run.add_argument(
        "--profile-dir",
        help="Path to the profile directory",
        default=PROFILE_DIR,
    )
    return parser.parse_args(args)


def cli(arguments: list[str] | None = None):
    """Run the reforger_backendless cli"""
    if arguments is None:
        arguments = sys.argv[1:]
    args = parse_arguments(arguments)
    return args.func(args)


def _run(args: argparse.Namespace):
    return run(
        args.config,
        args.podman,
        args.dry_run,
        args.host_network,
        args.extra_args,
        args.reforger_dir,
        args.profile_dir,
    )


def run(
    config_path: str,
    podman: bool,
    dry_run: bool,
    host_network: bool,
    extra_args: str,
    reforger_dir: str,
    profile_dir: str,
):
    """Run the program's main command"""
    logging.basicConfig(level=logging.INFO)

    for directory, name in [(reforger_dir, "reforger"), (profile_dir, "profile")]:
        if not os.path.exists(directory):
            logging.error(f"Error: The {name} directory '{directory}' does not exist.")
            return Exit.FAILURE

    logging.info(f"{host_network=}")

    server = BackendlessServer(
        config_path,
        podman,
        dry_run,
        host_network,
        extra_args,
        reforger_dir,
        profile_dir,
    )
    server.start()
    return Exit.SUCCESS
