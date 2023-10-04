# -*- coding: utf-8 -*-


from git_web_url.tests.data import CaseEnum
from git_web_url.find_repo_url import get_repo_url


def _test_get_repo_url_all():
    for name, case in CaseEnum.iter_items():
        # print(f"{name}: {case.origin_url}")
        repo_url, res = get_repo_url(case.origin_url)
        assert repo_url == case.repo_url


def _test_get_repo_url_edge_case():
    case = CaseEnum.bitbucket_enterprise_unknown_http.value
    repo_url, res = get_repo_url(case.origin_url)
    print(repo_url)
    print(case.repo_url)


def test_get_repo_url():
    print("")
    _test_get_repo_url_all()
    # _test_get_repo_url_edge_case()


if __name__ == "__main__":
    from git_web_url.tests import run_cov_test

    run_cov_test(__file__, "git_web_url.find_repo_url", preview=False)
