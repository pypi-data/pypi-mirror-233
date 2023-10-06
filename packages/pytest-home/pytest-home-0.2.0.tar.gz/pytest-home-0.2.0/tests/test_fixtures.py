import subprocess


def test_git_no_config(alt_home):
    """
    Ensure git finds config in alt_home.
    """
    alt_home.joinpath('.gitconfig').write_text(
        '[user]\nemail="joe@pie.com"', encoding='utf-8'
    )
    out = subprocess.check_output(['git', 'config', 'user.email'])
    out == 'joe@pie.com'
