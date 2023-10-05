from __future__ import annotations

import logging
import sys
from typing import TYPE_CHECKING
from typing import Callable
from typing import Iterable

from pyselector import key_manager

from pymarks import constants
from pymarks import database
from pymarks import display
from pymarks import scrape
from pymarks import utils
from pymarks.bookmark import RecordForDB
from pymarks.constants import BULLET
from pymarks.constants import ExitCode
from pymarks.constants import KeyCode

if TYPE_CHECKING:
    from sqlite3 import Cursor

    from pyselector.selector import MenuInterface

    from pymarks.bookmark import Bookmark
    from pymarks.bookmark import PromptFn


log = logging.getLogger(__name__)


@utils.timeit
def show_bookmarks(
    cursor: Cursor,
    menu: MenuInterface,
    prompt: PromptFn,
    items: Iterable[Bookmark],
) -> Bookmark:
    bookmark, return_code = display.items(prompt=prompt, items=items)
    keycode = KeyCode(return_code)

    while keycode != ExitCode(0):
        if keycode == KeyCode(1):
            sys.exit(1)
        try:
            keybind = menu.keybind.get_keybind_by_code(keycode)
            bookmark, keycode = keybind.callback(
                cursor,
                prompt,
                bookmark=bookmark,
                menu=menu,
                keybind=keybind,
            )
        except key_manager.KeybindError as err:
            log.warning(err)
            sys.exit(1)
    return bookmark


def create_bookmark(
    cursor: Cursor, prompt: PromptFn, **kwargs
) -> tuple[Bookmark | None, KeyCode]:
    kwargs['menu'].keybind.toggle_all()
    item = utils.read_from_clipboard()

    url, _ = prompt(
        prompt='New bookmark>',
        mesg='Reading <url> from clipboard',
        filter=item.strip(),
    )

    if not url:
        return None, KeyCode(1)

    if database.exists_in_database(cursor, url):
        database_name = database.get_database_path(cursor).name
        mesg = f'> Bookmark already exists on database {database_name!r}'
        display.warning(prompt, mesg)
        return None, KeyCode(1)

    tags, _ = prompt(
        prompt='Tags>',
        mesg=f'Add comma separated tags for <{url}>',
    )

    if not tags:
        tags = 'untitled,'

    title, desc = scrape.title_and_description(url)
    record = RecordForDB(url=url, tags=tags, title=title, description=desc)
    bookmark = database.create_bookmark(cursor, record)

    return bookmark, KeyCode(0)


def delete_bookmark(cursor: Cursor, prompt: PromptFn, b: Bookmark) -> None:
    if not display.confirmation(msg=f'Deleting {b.url}?', prompt=prompt):
        return
    database.remove_bookmark(cursor, b)
    sys.exit(0)


def tag_selector(
    cursor: Cursor, prompt: PromptFn, **kwargs
) -> tuple[str, KeyCode]:
    kwargs['menu'].keybind.toggle_all()
    min_tag_len = 2
    tags = database.get_tags_with_count(cursor)
    tag_selected, _ = prompt(items=tags, mesg='Filter by tag')

    if len(tag_selected.split()) < min_tag_len:
        err_msg = f'Invalid tag: {tag_selected!r}'
        raise ValueError(err_msg)

    tag = tag_selected.split()[0]
    log.debug('Selected tag: %s', tag)
    records = tuple(database.get_bookmarks_by_tag(cursor, tag))
    bookmark, code = prompt(items=records, mesg=f'Filter by tag <{tag}>')
    return bookmark, KeyCode(code)


def options_selector(
    # FIX: DRY my friend
    cursor: Cursor,
    prompt: PromptFn,
    **kwargs,
) -> tuple[Bookmark | None, KeyCode]:
    kwargs['menu'].keybind.toggle_all()
    bookmark: Bookmark = kwargs['bookmark']

    options_fn: dict[str, Callable] = {
        f'{BULLET} Edit': update_bookmark,
        f'{BULLET} Delete': delete_bookmark,
    }

    selected = display.options(
        tuple(options_fn.keys()),
        prompt=prompt,
        mesg=f'{BULLET} Actions for <{bookmark.url}>',
    )

    if selected is None:
        return None, KeyCode(1)

    if selected not in options_fn:
        return None, KeyCode(1)

    func = options_fn[selected]
    func(cursor, prompt, bookmark)
    return bookmark, KeyCode(0)


def update_bookmark(
    # FIX: DRY my friend
    cursor: Cursor,
    prompt: PromptFn,
    b: Bookmark,
) -> tuple[Bookmark | None, KeyCode]:
    options_fn: dict[str, Callable] = {
        f'{BULLET} Title': update_title,
        f'{BULLET} Description': update_desc,
        f'{BULLET} Tags': update_tags,
        f'{BULLET} URL': update_url,
        f'{BULLET} Fetch Title/Desc': fetch_and_update,
    }

    selected = display.options(
        tuple(options_fn.keys()),
        prompt,
        mesg=f'Options for <{b.url}>',
    )

    if selected is None:
        return None, KeyCode(1)

    if selected not in options_fn:
        return None, KeyCode(1)

    func = options_fn[selected]
    func(cursor, prompt, b)
    return b, KeyCode(0)


def update_title(
    cursor: Cursor, prompt: PromptFn, b: Bookmark
) -> tuple[Bookmark, KeyCode]:
    title, _ = prompt(
        mesg=f'{BULLET} URL: {b.url}', prompt='New title >', filter=b.title
    )

    if not title:
        title = ''

    database.update_bookmark_title(cursor, b.id, title)
    return b, KeyCode(0)


def update_desc(
    cursor: Cursor, prompt: PromptFn, b: Bookmark
) -> tuple[Bookmark, KeyCode]:
    desc, _ = prompt(
        mesg=f'{BULLET} URL: {b.url}',
        prompt='New Description >',
        filter=b.description,
    )

    if not desc:
        desc = ''

    database.update_bookmark_desc(cursor, b.id, desc)
    return b, KeyCode(0)


def update_tags(
    cursor: Cursor, prompt: PromptFn, b: Bookmark
) -> tuple[Bookmark, KeyCode]:
    tags, _ = prompt(
        mesg=f'{BULLET} URL: {b.url}', prompt='New Tags >', filter=b.tags
    )

    if not tags:
        tags = ','

    database.update_bookmark_tags(cursor, b.id, tags)
    return b, KeyCode(0)


def update_url(
    cursor: Cursor, prompt: PromptFn, b: Bookmark
) -> tuple[Bookmark, KeyCode]:
    url, _ = prompt(mesg=f'Updating URL: {b.url}', filter=b.url)
    database.update_bookmark_url(cursor, b.id, url)
    return b, KeyCode(0)


def fetch_and_update(
    cursor: Cursor, prompt: PromptFn, b: Bookmark
) -> tuple[Bookmark, KeyCode]:
    title, desc = scrape.title_and_description(b.url)
    confirmation = 'Accept changes?'

    items = (
        f'Title: {title}',
        f'Description: {desc}',
        confirmation,
    )

    if not display.confirmation(
        msg=f'Update {b.url} with data fetched?',
        prompt=prompt,
        items=items,
        confirmation=confirmation,
    ):
        return b, KeyCode(0)

    b.title = title
    b.description = desc
    database.update_bookmark(cursor, b)
    return b, KeyCode(0)


def item_detail(
    cursor: Cursor, prompt: PromptFn, **kwargs  # noqa: ARG001
) -> tuple[Bookmark, KeyCode]:
    kwargs['menu'].keybind.toggle_all()
    bookmark: Bookmark = kwargs['bookmark']
    detail = display.item_details(prompt, bookmark, icon=BULLET)
    utils.copy_to_clipboard(detail)
    return bookmark, KeyCode(1)


def database_selector(
    cursor: Cursor, prompt: PromptFn, **kwargs
) -> tuple[Bookmark, KeyCode]:
    kwargs['menu'].keybind.toggle_all()
    databases_path = tuple(constants.DATABASES_DIR.glob('*.db'))
    selected, _ = display.paths(list(map(str, databases_path)), prompt=prompt)
    database_path = constants.DATABASES_DIR / selected

    if not database_path.exists():
        err_msg = f'Database not found: {database_path}'
        log.error(err_msg)
        raise FileNotFoundError(err_msg)

    with database.open_database(database_path) as cursor:
        records = database.get_bookmarks_all(cursor)
        bookmark, keycode = display.items(prompt=prompt, items=tuple(records))

    return bookmark, KeyCode(0)
