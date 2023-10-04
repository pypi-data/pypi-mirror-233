# -*- coding: utf-8 -*-

from pathlib import Path
from configparser import ConfigParser
from .exc import NotGitRepoError


def locate_git_repo_dir(
    p_file: Path,
) -> Path:
    """
    Given a path of a file, find the git repository root directory.
    The root directory should have a ``.git`` directory.

    :param p_file
    """
    for p_dir in p_file.parents:
        p_git_config = Path(p_dir, ".git", "config")
        if p_git_config.exists():
            return p_dir
    raise NotGitRepoError(f"{p_file} is not in a git repository.")


def extract_remote_origin_url(
    p_git_config: Path,
):
    """
    Extract the remote origin url from the ``.git/config`` file.
    """
    config = ConfigParser()
    config.read(str(p_git_config))
    remote_origin_url = config['remote "origin"']["url"]
    return remote_origin_url


def extract_current_branch(
    p_git_head: Path,
) -> str:
    """
    Extract the current branch from the ``.git/HEAD`` file.
    """
    current_branch = p_git_head.read_text().strip().replace("ref: refs/heads/", "")
    return current_branch
