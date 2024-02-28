import asyncio
from contextlib import asynccontextmanager
from contextlib import contextmanager
import typing as t

from pwright import apw
from pwright import pw


async def run_async(agen: t.AsyncGenerator[apw.Page, None]):
    for _ in range(5):
        page = await anext(agen)
        await page.goto('https://www.google.com')
        print(id(page))
        # time.sleep(0.3)
    await agen.aclose()
    # await asyncio.sleep(10)


async def amain(headed=True):
    @asynccontextmanager
    async def agen_page():
        async with apw.pw_page(headed=headed) as page:
            yield page

    await run_async(apw.renewable(agen_page, 3))
    async with apw.auto_renew(agen_page, 3) as agen:
        await run_async(agen)


def run_sync(gen: t.Generator[pw.Page, None, None]):
    for _ in range(5):
        page = next(gen)
        page.goto('https://www.google.com')
        print(id(page))
        # time.sleep(0.3)
    gen.close()
    # time.sleep(10)


def main(headed=True):
    @contextmanager
    def gen_page():
        with pw.pw_page(headed=headed) as page:
            yield page

    run_sync(pw.renewable(gen_page, 3))
    with pw.auto_renew(gen_page, 3) as gen:
        run_sync(gen)


def test_async():
    asyncio.run(amain(headed=False))


def test_sync():
    main(headed=False)


if __name__ == '__main__':
    asyncio.run(amain())
    main()
