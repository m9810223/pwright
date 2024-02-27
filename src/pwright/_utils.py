from pathlib import Path


DEFAULT_INIT_SCRIPT = (
    # https://github.com/microsoft/playwright-python/issues/527#issuecomment-887182658
    # '''
    # navigator.webdriver = false
    # '''
    '''
    Object.defineProperty(navigator, 'webdriver', {get: () => false})
    '''
)


def relative_to(path: Path, other: Path):
    if path.is_relative_to(other):
        return path.relative_to(other)
    return path


def relative_to_cwd(path: Path):
    return relative_to(path, Path.cwd())
