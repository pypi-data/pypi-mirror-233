import pathlib
import platform

import pytest


@pytest.fixture
def tmp_home_dir(monkeypatch, tmp_path_factory):
    """
    >>> home = getfixture('tmp_home_dir')
    >>> list(home.iterdir())
    []
    >>> import pathlib
    >>> pathlib.Path('~').expanduser() == home
    True
    """
    return _set(monkeypatch, tmp_path_factory.mktemp('home'))


def _set(monkeypatch, path: pathlib.Path):
    """
    Set the home dir using a pytest monkeypatch context.
    """
    win = platform.system() == 'Windows'
    vars = ['HOME'] + win * ['USERPROFILE']
    for var in vars:
        monkeypatch.setenv(var, str(path))
    return path
