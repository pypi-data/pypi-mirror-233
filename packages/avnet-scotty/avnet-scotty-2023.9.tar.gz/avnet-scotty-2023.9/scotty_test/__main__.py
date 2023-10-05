# SPDX-FileCopyrightText: (C) 2023 Avnet Embedded GmbH
# SPDX-License-Identifier: GPL-3.0-only
"""scotty-test."""

import argparse
import os
import json
import logging
import sys

from colorama import Style
from colorama import Fore

from scotty_test.menu import show_menu
from scotty_test.storage import StorageClient
from scotty_test.runner import Runner
from scotty_test.reporter import Reporter


class ScottyTestLoggingFormatter(logging.Formatter):
    """scotty-test custom logging formatter."""

    format = "%(levelname)s:%(message)s"
    format_exp = "%(levelname)s:%(message)s (%(filename)s:%(lineno)d)"

    FORMATS = {
        logging.DEBUG: Fore.WHITE + format + Style.RESET_ALL,
        logging.INFO: Fore.WHITE + format + Style.RESET_ALL,
        logging.WARNING: Fore.YELLOW + format + Style.RESET_ALL,
        logging.ERROR: Fore.RED + format + Style.RESET_ALL,
        logging.CRITICAL: Fore.RED + format_exp + Style.RESET_ALL
    }

    def format(self, record):
        """Format a message."""
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


def parse_args() -> argparse.Namespace:
    """Argparse handler."""
    parser = argparse.ArgumentParser()
    parser.add_argument('--token', default=os.environ.get('SAS_TOKEN'),
                        help='Azure Storage connection string')
    parser.add_argument('--ghcruser', default=os.environ.get('GHCR_USER'),
                        help='Github username')
    parser.add_argument('--ghcrtoken', default=os.environ.get('GHCR_TOKEN'),
                        help='Github personal access token')
    parser.add_argument('--sdkpath', default='', help='Path to custom SDK')
    parser.add_argument(
        '--sdcard', choices=['manual', 'sdwire'], default='manual', help='SDCard handler')
    return parser.parse_args()


def main():
    """Entry point."""
    # configure logging first
    logger = logging.getLogger('scotty-test')
    handler = logging.StreamHandler()
    handler.setFormatter(ScottyTestLoggingFormatter())
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

    args = parse_args()
    if not args.token:
        logging.getLogger('scotty-test').error(
            'You need to pass an Azure blob storage token by either "--token" or via "SAS_TOKEN" environment variable')
        sys.exit(1)
    if not args.ghcruser:
        logging.getLogger('scotty-test').warning(
            '"GHCR_USER" or "--ghcruser" is not set. Some tests will likely fail')
    if not args.ghcrtoken:
        logging.getLogger('scotty-test').warning(
            '"GHCR_TOKEN" or "--ghcrtoken" is not set. Some tests will likely fail')
    _storage = StorageClient(args.token)

    _run_config = None
    _selected_version = None
    while not _run_config:
        _selected_version = show_menu('Select a version', sorted(
            [(x, x) for x in _storage.list_dirs('')]))
        try:
            with open(_storage.download(f'{_selected_version}/build-mapping.json')) as i:
                _run_config = json.load(i)
        except Exception as e:
            logging.getLogger('scotty-test').exception(e)

    # set preferred container version in test
    os.environ['GHCR_CONTAINER_VERSION'] = _selected_version
    # set github container registry credentials
    os.environ['GHCR_USER'] = args.ghcruser or ''
    os.environ['GHCR_TOKEN'] = args.ghcrtoken or ''

    results = []
    while True:
        _selected_machine = show_menu(
            'Select a machine', sorted([x for x in _run_config.keys()]))
        _selected_image = show_menu('Select an image', sorted(
            [(k, {k: v}) for k, v in _run_config[_selected_machine].items()]))

        _runner = Runner(_storage, _selected_version,
                         _selected_machine, _selected_image, args.sdcard, args.sdkpath)
        results.append(_runner.run())

        if not show_menu('Do you want to test another image?', entries=[('Yes', True), ('No', False)]):
            break

    r = Reporter(_storage, _selected_version, results)
    if r.run():
        logging.getLogger('scotty-test').info(
            'Report generated - Please open a PR at https://github.com/avnet-embedded/simplecore-tools')
    else:
        logging.getLogger(
            'scotty-test').debug('Nothing changed since the last report - All good!')


if __name__ == '__main__':
    main()
