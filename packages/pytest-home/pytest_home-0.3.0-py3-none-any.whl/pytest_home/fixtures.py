import pathlib
import platform

import pytest


@pytest.fixture
def alt_home(monkeypatch, tmp_path_factory):
    """
    >>> home = getfixture('alt_home')
    >>> list(home.iterdir())
    []
    >>> import pathlib
    >>> pathlib.Path('~').expanduser() == home
    True
    """
    return set(monkeypatch, tmp_path_factory.mktemp('home'))


def set(monkeypatch, path: pathlib.Path):
    """
    Set the home dir using a pytest monkeypatch context.
    """
    win = platform.system() == 'Windows'
    vars = ['HOME'] + win * ['USERPROFILE']
    for var in vars:
        monkeypatch.setenv(var, str(path))
    return path
