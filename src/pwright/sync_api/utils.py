from contextlib import contextmanager
import logging
from pathlib import Path
import typing as t

from .._utils import relative_to_cwd
from ._apis import Page


logger = logging.getLogger(__name__)


T = t.TypeVar('T')


@contextmanager
def auto_renew(p: t.Callable[..., t.ContextManager[T]], n: int):
    yield renewable(p, n)


def renewable(p: t.Callable[..., t.ContextManager[T]], n: int):
    while True:
        with p() as obj:
            for _ in range(n):
                yield obj


def screenshot(
    page: Page,
    *,
    file=Path.cwd() / '.temp' / 'screenshot.png',
):
    file.parent.mkdir(parents=True, exist_ok=True)
    file.write_bytes(page.screenshot())
    logger.info(f' -> screenshot: ./{relative_to_cwd(file)}')
