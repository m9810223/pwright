from contextlib import contextmanager
import logging
import typing as t

from .._constants import DEFAULT_INIT_SCRIPT
from ._apis import playwright


logger = logging.getLogger(__name__)


@contextmanager
def playwright_browser(*, timeout: t.Optional[float] = None, headed: t.Optional[bool] = None):
    # https://playwright.dev/python/docs/test-runners#fixtures
    with playwright() as _playwright:
        logger.debug(f'{_playwright = }')
        with _playwright.chromium.launch(timeout=timeout, headless=not headed) as browser:
            browser_type = browser.browser_type
            logger.debug(f'{browser_type = }')
            logger.debug(f'{browser = }')
            browser_name = browser_type.name
            logger.debug(f'{browser_name = }')
            yield browser


@contextmanager
def playwright_context(
    *,
    # [browser]
    timeout: t.Optional[float] = None,
    headed: t.Optional[bool] = None,
    # [context]
    user_agent: t.Optional[str] = None,
    base_url: t.Optional[str] = None,
    # [context.tracing]
    tracing=False,
    screenshots=True,
    snapshots=True,
    sources=True,
    path='trace.zip',
):
    with playwright_browser(timeout=timeout, headed=headed) as browser:
        with browser.new_context(user_agent=user_agent, base_url=base_url) as context:
            logger.debug(f'{context = }')
            if tracing:
                context.tracing.start(screenshots=screenshots, snapshots=snapshots, sources=sources)
            yield browser, context
            if tracing:
                context.tracing.stop(path=path)


@contextmanager
def playwright_page(
    *,
    # [browser]
    timeout: t.Optional[float] = None,
    headed: t.Optional[bool] = None,
    # [context]
    user_agent: t.Optional[str] = None,
    base_url: t.Optional[str] = None,
    # [context.tracing]
    tracing=False,
    screenshots=True,
    snapshots=True,
    sources=True,
    path='trace.zip',
    # [page]
    init_script=DEFAULT_INIT_SCRIPT,
):
    with playwright_context(
        timeout=timeout,
        headed=headed,
        user_agent=user_agent,
        base_url=base_url,
        tracing=tracing,
        screenshots=screenshots,
        snapshots=snapshots,
        sources=sources,
        path=path,
    ) as (browser, context):
        with context.new_page() as page:
            page.add_init_script(init_script)
            logger.debug(f'{page = }')
            yield browser, context, page
