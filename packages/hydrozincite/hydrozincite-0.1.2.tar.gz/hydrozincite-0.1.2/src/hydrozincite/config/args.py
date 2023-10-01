#!/usr/bin/env python3

import argparse
import logging

log_level = {
    "CRITICAL": logging.CRITICAL,
    "ERROR": logging.ERROR,
    "WARN": logging.WARNING,
    "INFO": logging.INFO,
    "DEBUG": logging.DEBUG,
}


def get_args():
    parser = argparse.ArgumentParser()

    sub = parser.add_subparsers(dest="sub")

    parser.add_argument(
        "-l",
        "--log",
        choices=log_level.keys(),
        default="WARN",
        help=("Set level log"),
        dest="log",
    )

    parser.add_argument("-c", "--conf", help=("Path for config file"), dest="conf")

    parser.add_argument(
        "-r", "--repositories", help=("Path for git repositories"), dest="repositories"
    )

    parser.add_argument("-o", "--output", help=("Output directory"), dest="output")

    parser.add_argument("-t", "--title", help=("Title for HMTL page"), dest="title")

    parser.add_argument(
        "-u", "--clone-url", help=("Clone URL for git repositories"), dest="clone_url"
    )

    info = sub.add_parser("info", help="Get info for repositories")  # noqa: F841

    hook = sub.add_parser("hook", help="Set hook")  # noqa: F841

    hook.add_argument(
        "-w", "--write", help=("Write hooks"), dest="write", action="store_true"
    )

    args = parser.parse_args()
    return args


args = get_args()
