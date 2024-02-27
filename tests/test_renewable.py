import asyncio
from contextlib import asynccontextmanager
from contextlib import contextmanager

from pwright import apw
from pwright import pw


def main(headed=True):
    @contextmanager
    def gen_page():
        with pw.pw_page(headed=headed) as (_, _, page):
            yield page

    gen = pw.renewable(gen_page, 3)
    for _ in range(5):
        page = next(gen)
        page.goto('https://www.google.com')
        print(id(page))
        # time.sleep(0.3)
    gen.close()
    # time.sleep(10)


async def amain(headed=True):
    @asynccontextmanager
    async def agen_page():
        async with apw.pw_page(headed=headed) as (_, _, page):
            yield page

    agen = apw.renewable(agen_page, 3)
    for _ in range(5):
        page = await anext(agen)
        await page.goto('https://www.google.com')
        print(id(page))
        # time.sleep(0.3)
    await agen.aclose()
    # await asyncio.sleep(10)


def test_sync():
    main(headed=False)


def test_async():
    asyncio.run(amain(headed=False))


if __name__ == '__main__':
    main()
    asyncio.run(amain())
