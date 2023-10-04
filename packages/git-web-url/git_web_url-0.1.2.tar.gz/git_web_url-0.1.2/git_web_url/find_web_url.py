# -*- coding: utf-8 -*-

"""
This module implements the logic to find the corresponding web url
of a local file in a local git repo.

Basically, it locate the ``.git/config`` file, extract the remote origin url,
parse it, and then generate the web url.
"""

from pathlib import Path

from .vendor.git_cli import get_git_commit_id_from_git_cli
from .utils import (
    locate_git_repo_dir,
    extract_remote_origin_url,
    extract_current_branch,
)
from .parser import PlatformEnum
from .find_repo_url import parse_aws_codecommit_remote_origin_url, get_repo_url


def get_web_url(
    path: Path,
):
    """
    This module implements the logic to find the corresponding web url
    of a local file in a local git repo.
    """
    p_git_repo_dir = locate_git_repo_dir(path)
    remote_origin_url = extract_remote_origin_url(
        p_git_repo_dir.joinpath(".git", "config")
    )
    git_branch = extract_current_branch(p_git_repo_dir.joinpath(".git", "HEAD"))
    repo_url, res = get_repo_url(remote_origin_url)

    relative_path = str(path.relative_to(p_git_repo_dir))
    if res.platform is PlatformEnum.aws_codecommit:
        aws_region = parse_aws_codecommit_remote_origin_url(remote_origin_url)
        return f"{repo_url}/browse/refs/heads/{git_branch}/--/{relative_path}?region={aws_region}"
    elif res.platform is PlatformEnum.bitbucket: # bitbucket saas
        if res.domain == "bitbucket.org":
            commit_id = get_git_commit_id_from_git_cli(p_git_repo_dir)
            return f"{repo_url}/src/{commit_id}/{relative_path}?at={git_branch}"
        else: # bitbucket server
            return f"{repo_url}/browse/{relative_path}?at=refs/heads/{git_branch}"
    else:
        if path.is_file():
            return f"{repo_url}/blob/{git_branch}/{relative_path}"
        else:
            return f"{repo_url}/tree/{git_branch}/{relative_path}"
