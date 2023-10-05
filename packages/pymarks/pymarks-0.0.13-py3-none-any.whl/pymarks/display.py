from __future__ import annotations

import logging
import typing
from typing import Iterable

if typing.TYPE_CHECKING:
    from pathlib import Path

    from pymarks.bookmark import Bookmark
    from pymarks.bookmark import PromptFn

log = logging.getLogger(__name__)


def items(
    items: Iterable[Bookmark] | list[str],
    prompt: PromptFn,
) -> tuple[Bookmark, int]:
    item, code = prompt(items=items)
    return item, code


def paths(
    items: Iterable[Bookmark] | list[str],
    prompt: PromptFn,
) -> tuple[Path, int]:
    item, code = prompt(items=items)
    return item, code


def warning(prompt: PromptFn, msg: str) -> None:
    prompt([msg])


def confirmation(
    prompt: PromptFn,
    msg: str,
    prompt_msg: str = 'Confirm>',
    items: tuple[str, ...] | None = None,
    confirmation: str = 'Yes',
) -> bool:
    if not items:
        items = ('Yes', 'No')

    item, _ = prompt(
        case_sensitive=True,
        prompt=prompt_msg,
        items=items,
        mesg=msg,
    )
    log.debug('Confirmation: %s', item)
    return item == confirmation


def options(
    choices: tuple[str, ...], prompt: PromptFn, mesg: str
) -> str | None:
    item, _ = prompt(items=choices, mesg=mesg)
    if not item:
        return None
    return item


def item_details(prompt: PromptFn, b: Bookmark, icon: str) -> str:
    mesg = f'Details for <{b.url}>'
    info = (
        f'{icon} ID: {b.id}',
        f'{icon} Title: {b.title}',
        f'{icon} URL: {b.url}',
        f'{icon} Description: {b.description}',
        f'{icon} Tags: {b.tags}',
    )
    item, _ = prompt(items=info, mesg=mesg)
    return item
