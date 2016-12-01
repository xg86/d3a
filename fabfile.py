import os
import shutil
from pathlib import Path

from fabric.colors import blue, green, yellow
from fabric.context_managers import hide
from fabric.decorators import task
from fabric.operations import local
from fabric.tasks import execute
from fabric.utils import abort, puts


HERE = Path().resolve()
REQ_DIR = HERE / 'requirements'


def _ensure_captainhook():
    hook = Path(".git/hooks/pre-commit")
    captainhook_installed = False
    if hook.exists():
        captainhook_installed = ("CAPTAINHOOK IDENTIFIER" in hook.read_text())
    if not captainhook_installed:
        puts(yellow("Configuring 'captainhook' git pre-commit hooks"))
        with hide('running', 'stdout'):
            local("captainhook install --use-virtualenv-python")
    shutil.copy('.support/solium_checker.py', '.git/hooks/checkers/')


def _pre_check():
    if 'VIRTUAL_ENV' not in os.environ:
        abort('No active virtualenv found. Please create / activate one before continuing.')
    try:
        import piptools  # noqa
    except ImportError:
        with hide('running', 'stdout'):
            puts(yellow("Installing 'pip-tools'"), show_prefix=True)
            local("pip install pip-tools")


def _post_check():
    _ensure_captainhook()


@task
def compile():
    """Update list of requirements"""
    _pre_check()
    with hide('running', 'stdout'):
        puts(green("Updating requirements"), show_prefix=True)
        for file in REQ_DIR.glob('*.in'):
            puts(blue("  - {}".format(file.name.replace(".in", ""))))
            local('pip-compile --no-index --rebuild {0}'.format(file.relative_to(HERE)))


@task(default=True)
def sync():
    """Ensure installed packages match requirements"""
    _pre_check()
    with hide('running'):
        puts(green("Syncing requirements to local packages"), show_prefix=True)
        local(
            'pip-sync {}'.format(
                " ".join(
                    str(f.relative_to(HERE))
                    for f in REQ_DIR.glob('*.txt')
                )
            )
        )
        local('pip install --no-deps -e .')
    _post_check()


@task
def reqs():
    """'compile' then 'sync'"""
    execute(compile)
    execute(sync)