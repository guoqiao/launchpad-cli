#!/usr/bin/env python3

from os import getenv
import subprocess
import logging

import click

LOG_FORMAT = '%(asctime)s - %(levelname)s - %(module)s - %(message)s'
LOG = logging.getLogger(__name__)



LAUNCHPAD_USER = getenv('LAUNCHPAD_USER') or getenv('USER')
assert LAUNCHPAD_USER


def run_cmd(cmd):
    LOG.debug('running cmd: %s', ' '.join(cmd))
    subprocess.check_call(cmd)


def repo_clone(name):
    url = f'git+ssh://{LAUNCHPAD_USER}@git.launchpad.net/{name}'
    run_cmd(['git', 'clone', url])



@click.group()
@click.option('-v', '--verbose', is_flag=True, default=False, help='Print debug logs')
@click.option('-q', '--quiet', is_flag=True, default=False, help='Print warning logs')
def lp(verbose, quiet):
    if verbose:
        level = 'DEBUG'
    elif quiet:
        level = 'WARNING'
    else:
        level = 'INFO'
    logging.basicConfig(level=level, format=LOG_FORMAT)



@lp.group()
def repo():
    pass


@repo.command()
@click.argument('repo')
@click.argument('directory', required=False)
def clone(repo, directory):

    branch = None
    user = None

    if ':' in repo:
        repo, branch = repo.split(':', maxsplit=1)
    if '/' in repo:
        user, repo = repo.split('/', maxsplit=1)

    if user:
        url = f'git+ssh://{LAUNCHPAD_USER}@git.launchpad.net/~{user}/{repo}'
    else:
        url = f'git+ssh://{LAUNCHPAD_USER}@git.launchpad.net/{repo}'

    cmd = ['git', 'clone']

    if branch:
        cmd += ['-b', branch]
    cmd.append(url)
    if directory:
        cmd.append(directory)
    run_cmd(cmd)


@lp.group()
def merge():
    pass


@lp.group()
def bug():
    pass


if __name__ == '__main__':
    lp()
