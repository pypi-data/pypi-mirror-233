# -*- coding: utf-8 -*-


from git_web_url.tests.data import CaseEnum
from git_web_url.parser import parse


def _test_parse_all():
    for name, case in CaseEnum.iter_items():
        # print(f"{name}: {case.origin_url}")
        result = parse(case.origin_url)
        assert result.protocol == case.protocol
        assert result.platform == case.platform
        assert result.domain == case.domain
        assert result.owner == case.owner
        assert result.repo == case.repo


def _test_parse_edge_case():
    case = CaseEnum.aws_codecommit_grc.value
    result = parse(case.origin_url, debug=True)
    print(f"protocol: {result.protocol!r} vs {case.protocol!r}")
    print(f"platform: {result.platform!r} vs {case.platform!r}")
    print(f"domain: {result.domain!r} vs {case.domain!r}")
    print(f"owner: {result.owner!r} vs {case.owner!r}")
    print(f"repo: {result.repo!r} vs {case.repo!r}")


def test_get_repo_url():
    print("")
    _test_parse_all()
    # _test_parse_edge_case()


if __name__ == "__main__":
    from git_web_url.tests import run_cov_test

    run_cov_test(__file__, "git_web_url.parser", preview=False)
