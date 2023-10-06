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
    win = platform.system() == 'Windows'
    vars = ['HOME'] + win * ['USERPROFILE']
    home = tmp_path_factory.mktemp('home')
    for var in vars:
        monkeypatch.setenv(var, str(home))
    return home
