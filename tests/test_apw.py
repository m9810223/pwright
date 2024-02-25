import asyncio

from pwright import apw


def test_playwright_page():
    async def f():
        async with apw.playwright_page() as (browser, context, page):
            await page.goto('https://playwright.dev/')
            title = await page.title()
            return title

    title = asyncio.run(f())
    assert 'Playwright' in title
