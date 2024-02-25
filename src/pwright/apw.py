from contextlib import asynccontextmanager
import logging
from pathlib import Path
import typing as t

from playwright.async_api import Browser as Browser
from playwright.async_api import BrowserContext as BrowserContext
from playwright.async_api import Dialog as Dialog
from playwright.async_api import ElementHandle as ElementHandle
from playwright.async_api import Page as Page
from playwright.async_api import Playwright as Playwright
from playwright.async_api import Route as Route
from playwright.async_api import TimeoutError as TimeoutError
from playwright.async_api import async_playwright as playwright


Eh = ElementHandle


logger = logging.getLogger(__name__)


async def screenshot(
    page: Page,
    *,
    file=Path.cwd() / '.temp' / 'screenshot.png',
):
    file.parent.mkdir(parents=True, exist_ok=True)
    file.write_bytes(await page.screenshot())
    logger.info(f' -> screenshot: ./{file.relative_to(Path.cwd())}')


@asynccontextmanager
async def playwright_page(
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
    async with playwright_context(
        timeout=timeout, headed=headed, user_agent=user_agent, base_url=base_url
    ) as (browser, context):
        if tracing:
            await context.tracing.start(
                screenshots=screenshots, snapshots=snapshots, sources=sources
            )
        async with await context.new_page() as page:
            await page.add_init_script(
                # https://github.com/microsoft/playwright-python/issues/527#issuecomment-887182658
                # '''
                # navigator.webdriver = false
                # '''
                '''
                Object.defineProperty(navigator, 'webdriver', {get: () => false})
                '''
            )
            logger.debug(f'{page = }')
            yield browser, context, page
        if tracing:
            await context.tracing.stop(path=path)


@asynccontextmanager
async def playwright_context(
    *,
    # [browser]
    timeout: t.Optional[float] = None,
    headed: t.Optional[bool] = None,
    # [context]
    user_agent: t.Optional[str] = None,
    base_url: t.Optional[str] = None,
):
    async with playwright_browser(timeout=timeout, headed=headed) as browser:
        async with await browser.new_context(user_agent=user_agent, base_url=base_url) as context:
            logger.debug(f'{context = }')
            yield browser, context


@asynccontextmanager
async def playwright_browser(
    *,
    # [browser]
    timeout: t.Optional[float] = None,
    headed: t.Optional[bool] = None,
):
    # https://playwright.dev/python/docs/test-runners#fixtures
    async with playwright() as _playwright:
        logger.debug(f'{_playwright = }')
        async with await _playwright.chromium.launch(
            timeout=timeout, headless=not headed
        ) as browser:
            browser_type = browser.browser_type
            logger.debug(f'{browser_type = }')
            logger.debug(f'{browser = }')
            browser_name = browser_type.name
            logger.debug(f'{browser_name = }')
            yield browser
