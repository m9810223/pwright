from pwright import pw


def test_playwright_page():
    def f():
        with pw.pw_page() as page:
            page.goto('https://playwright.dev/')
            title = page.title()
            return title

    title = f()
    assert 'Playwright' in title
