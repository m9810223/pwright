from contextlib import asynccontextmanager
import typing as t

from .._constants import DEFAULT_INIT_SCRIPT
from ._cms import playwright_browser
from ._cms import playwright_context
from ._cms import playwright_page


pw_browser = playwright_browser


@asynccontextmanager
async def pw_context(
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
        # [browser]
        timeout=timeout,
        headed=headed,
        # [context]
        user_agent=user_agent,
        base_url=base_url,
        # [context.tracing]
        tracing=tracing,
        screenshots=screenshots,
        snapshots=snapshots,
        sources=sources,
        path=path,
    ) as (_, context):
        yield context


@asynccontextmanager
async def pw_page(
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
    async with playwright_page(
        # [browser]
        timeout=timeout,
        headed=headed,
        # [context]
        user_agent=user_agent,
        base_url=base_url,
        # [context.tracing]
        tracing=tracing,
        screenshots=screenshots,
        snapshots=snapshots,
        sources=sources,
        path=path,
        # [page]
        init_script=init_script,
    ) as (_, _, page):
        yield page
