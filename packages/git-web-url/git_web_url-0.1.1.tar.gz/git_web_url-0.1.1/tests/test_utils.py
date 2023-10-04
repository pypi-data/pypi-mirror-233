# -*- coding: utf-8 -*-

import pytest
import typing as T
import enum
import dataclasses
from pathlib import Path

from git_web_url.utils import (
    NotGitRepoError,
    locate_git_repo_dir,
    extract_remote_origin_url,
    extract_current_branch,
)

dir_tests = Path(__file__).absolute().parent
dir_project_root = dir_tests.parent
path_git_config = dir_tests.joinpath("test_git_config")
path_git_head = dir_tests.joinpath("test_git_HEAD")


def test_locate_git_repo_dir():
    assert locate_git_repo_dir(Path(__file__).absolute()) == dir_project_root
    with pytest.raises(NotGitRepoError):
        locate_git_repo_dir(Path.home().joinpath("hello", "world", "file.txt"))


def test_extract_remote_origin_url():
    url = "https://github.com/example-user/example-repo.git"
    assert extract_remote_origin_url(path_git_config) == url


def test_extract_current_branch():
    assert extract_current_branch(path_git_head) == "main"


if __name__ == "__main__":
    from git_web_url.tests import run_cov_test

    run_cov_test(__file__, "git_web_url.utils", preview=False)
