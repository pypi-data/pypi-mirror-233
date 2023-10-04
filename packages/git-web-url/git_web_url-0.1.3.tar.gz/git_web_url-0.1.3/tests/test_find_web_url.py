# -*- coding: utf-8 -*-

from pathlib import Path
from git_web_url.find_web_url import get_web_url

dir_doc = Path.home().joinpath("Documents")


def _test_get_web_url():
    print(get_web_url(Path(__file__)))
    print(get_web_url(Path(__file__).absolute().parent.parent))


def _test_get_web_url_edge_case():
    print(get_web_url(dir_doc / "CodeCommit" / "multi_env-project" / "README.rst"))
    print(get_web_url(dir_doc / "BitBucket" / "public" / "license.txt"))
    print(get_web_url(dir_doc / "GitHub" / "afwf_github-project" / "main.py"))
    print(get_web_url(dir_doc / "GitLab" / "woob" / "README.rst"))


def test_get_repo_url():
    print("")
    _test_get_web_url()
    # _test_get_web_url_edge_case()


if __name__ == "__main__":
    from git_web_url.tests import run_cov_test

    run_cov_test(__file__, "git_web_url.find_web_url", preview=False)
