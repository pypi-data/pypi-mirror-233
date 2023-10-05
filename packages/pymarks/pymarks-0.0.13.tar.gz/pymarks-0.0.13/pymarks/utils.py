# helpers.py

from __future__ import annotations

import logging
import shlex
import shutil
import subprocess
import time
from functools import wraps
from typing import Callable
from typing import NamedTuple

from pymarks import constants
from pymarks import database
from pymarks import files
from pymarks.constants import ExitCode

log = logging.getLogger(__name__)


class BookmarkNotValidError(Exception):
    pass


class Clipboard(NamedTuple):
    copy: str
    paste: str


CLIPBOARDS: dict[str, Clipboard] = {
    'xclip': Clipboard(
        copy='xclip -selection clipboard',
        paste='xclip -selection clipboard -o',
    ),
    'xsel': Clipboard(
        copy='xsel -b -i',
        paste='xsel -b -o',
    ),
    'wl-copy': Clipboard(
        copy='wl-copy',
        paste='wl-paste',
    ),
}


def get_clipboard() -> Clipboard:
    for command, clipboard in CLIPBOARDS.items():
        if shutil.which(command):
            log.info(f'clipboard command: {clipboard!r}')
            return clipboard
    err_msg = 'No suitable clipboard command found.'
    log.error(err_msg)
    raise FileNotFoundError(err_msg)


def parse_tags(tags: str) -> str:
    tags = ','.join([string.strip() for string in tags.split(',')])
    if tags.endswith(','):
        return tags
    return tags + ','


def read_from_clipboard() -> str:
    """Read clipboard to add a new bookmark."""
    args = shlex.split(get_clipboard().paste)
    proc = subprocess.Popen(args, stdout=subprocess.PIPE)
    if proc.stdout is not None:
        data = proc.stdout.read()
        proc.stdout.close()
        return data.decode('utf-8')
    err_msg = 'Failed to start subprocess.'
    log.error(err_msg)
    raise RuntimeError(err_msg)


def copy_to_clipboard(item: str) -> ExitCode:
    """Copy selected item to the system clipboard."""
    data = item.encode('utf-8', errors='ignore')
    args = shlex.split(get_clipboard().copy)
    try:
        with subprocess.Popen(args, stdin=subprocess.PIPE) as proc:
            proc.stdin.write(data)  # type: ignore[union-attr]
            log.debug("Copied '%s' to clipboard", item)
    except subprocess.SubprocessError as e:
        log.error("Failed to copy '%s' to clipboard: %s", item, e)
        return ExitCode(1)
    return ExitCode(0)


def setup_project() -> None:
    files.mkdir(constants.PYMARKS_HOME)
    files.mkdir(constants.DATABASES_DIR)
    files.mkdir(constants.PYMARKS_BACKUP_DIR)
    files.touch(constants.DB_DEFAULT_FILE)
    database.init_database(constants.DB_DEFAULT_FILE)
    database.check_backup_files()


def timeit(func: Callable) -> Callable:
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        log.info(
            f'execution time: {func.__name__}. took {total_time:.4f} seconds'
        )
        return result

    return timeit_wrapper
