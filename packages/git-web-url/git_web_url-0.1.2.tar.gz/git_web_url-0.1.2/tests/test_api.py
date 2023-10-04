# -*- coding: utf-8 -*-

from git_web_url import api


def test():
    _ = api
    _ = api.PlatformEnum
    _ = api.ProtocolEnum
    _ = api.get_web_url


if __name__ == "__main__":
    from git_web_url.tests import run_cov_test

    run_cov_test(__file__, "git_web_url.api", preview=False)
