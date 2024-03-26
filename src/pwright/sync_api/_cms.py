from contextlib import contextmanager
import logging
from pathlib import Path
import typing as t

from .._constants import INIT_SCRIPT_HIDE_NAVIGATOR
from .._typealiases import SecondsT
from .._utils import to_milliseconds
from ._apis import ProxySettings
from ._apis import playwright


logger = logging.getLogger(__name__)


@contextmanager
def playwright_browser(
    *,
    # [browser]
    executable_path: t.Optional[t.Union[str, Path]] = None,
    headed: t.Optional[bool] = None,
    proxy: t.Optional[ProxySettings] = None,
    slow_mo: t.Optional[SecondsT] = None,
    traces_dir: t.Optional[t.Union[str, Path]] = None,
):
    # https://playwright.dev/python/docs/test-runners#fixtures
    with playwright() as _playwright:
        logger.debug(f'{_playwright = }')
        with _playwright.chromium.launch(
            executable_path=executable_path,
            headless=not headed,
            proxy=proxy,
            slow_mo=to_milliseconds(slow_mo),
            traces_dir=traces_dir,
        ) as browser:
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
    executable_path: t.Optional[t.Union[str, Path]] = None,
    headed: t.Optional[bool] = None,
    proxy: t.Optional[ProxySettings] = None,
    slow_mo: t.Optional[SecondsT] = None,
    traces_dir: t.Optional[t.Union[str, Path]] = None,
    # [context]
    no_viewport: t.Optional[bool] = True,
    user_agent: t.Optional[str] = None,
    is_mobile: t.Optional[bool] = None,
    # proxy: t.Optional[ProxySettings] = None,
    # [context.tracing]
    tracing=False,
    snapshots=True,
    screenshots=True,
    sources=True,
    path='trace.zip',
):
    with playwright_browser(
        executable_path=executable_path,
        headed=headed,
        proxy=proxy,
        slow_mo=slow_mo,
        traces_dir=traces_dir,
    ) as browser:
        with browser.new_context(
            no_viewport=no_viewport,
            user_agent=user_agent,
            is_mobile=is_mobile,
            proxy=proxy,
        ) as context:
            logger.debug(f'{context = }')
            if tracing:
                context.tracing.start(
                    snapshots=snapshots,
                    screenshots=screenshots,
                    sources=sources,
                )
            yield browser, context
            if tracing:
                context.tracing.stop(
                    path=path,
                )


@contextmanager
def playwright_page(
    *,
    # [browser]
    executable_path: t.Optional[t.Union[str, Path]] = None,
    headed: t.Optional[bool] = None,
    proxy: t.Optional[ProxySettings] = None,
    slow_mo: t.Optional[SecondsT] = None,
    traces_dir: t.Optional[t.Union[str, Path]] = None,
    # [context]
    no_viewport: t.Optional[bool] = True,
    user_agent: t.Optional[str] = None,
    is_mobile: t.Optional[bool] = None,
    # proxy: t.Optional[ProxySettings] = None,
    # [context.tracing]
    tracing=False,
    snapshots=True,
    screenshots=True,
    sources=True,
    path='trace.zip',
    # [page]
    default_navigation_timeout: t.Optional[SecondsT] = None,
    default_timeout: t.Optional[SecondsT] = None,
    init_script: t.Optional[str] = INIT_SCRIPT_HIDE_NAVIGATOR,
    init_script_path: t.Optional[t.Union[str, Path]] = None,
):
    with playwright_context(
        executable_path=executable_path,
        headed=headed,
        proxy=proxy,
        slow_mo=slow_mo,
        traces_dir=traces_dir,
        no_viewport=no_viewport,
        user_agent=user_agent,
        is_mobile=is_mobile,
        tracing=tracing,
        snapshots=snapshots,
        screenshots=screenshots,
        sources=sources,
        path=path,
    ) as (browser, context):
        with context.new_page() as page:
            if default_navigation_timeout is not None:
                page.set_default_navigation_timeout(
                    timeout=to_milliseconds(default_navigation_timeout),
                )
            if default_timeout is not None:
                page.set_default_timeout(
                    timeout=to_milliseconds(default_timeout),
                )
            page.add_init_script(
                script=init_script,
                path=init_script_path,
            )
            logger.debug(f'{page = }')
            yield browser, context, page
