# -*- coding: utf-8 -*-

import typing as T
import enum
import dataclasses

from ..parser import (
    ProtocolEnum,
    PlatformEnum,
)


@dataclasses.dataclass
class Case:
    """
    Represent a ground truth test case for a git url.

    :param origin_url: the remote origin url in the ``.git/config`` file.
    :param repo_url: the desired web url.
    :param platform: the desired git system.
    """

    origin_url: str = dataclasses.field()
    repo_url: str = dataclasses.field()
    protocol: str = dataclasses.field()
    platform: str = dataclasses.field()
    domain: str = dataclasses.field()
    owner: str = dataclasses.field()
    repo: str = dataclasses.field()


class CaseEnum(enum.Enum):
    """
    Enumerate all the test cases.
    """

    # GitHub Saas
    github_saas_http = Case(
        origin_url="https://github.com/user-name/repo-name.git",
        repo_url="https://github.com/user-name/repo-name",
        protocol=ProtocolEnum.https,
        platform=PlatformEnum.github,
        domain="github.com",
        owner="user-name",
        repo="repo-name",
    )
    github_saas_token = Case(
        origin_url="https://my_github_token@github.com/user-name/repo-name.git",
        repo_url="https://github.com/user-name/repo-name",
        protocol=ProtocolEnum.https,
        platform=PlatformEnum.github,
        domain="github.com",
        owner="user-name",
        repo="repo-name",
    )
    github_saas_ssh = Case(
        origin_url="ssh://git@github.com:user-name/repo-name.git",
        repo_url="https://github.com/user-name/repo-name",
        protocol=ProtocolEnum.ssh,
        platform=PlatformEnum.github,
        domain="github.com",
        owner="user-name",
        repo="repo-name",
    )

    # GitHub Enterprise
    github_enterprise_http = Case(
        origin_url="https://github.mycompany.net/team-name/repo-name.git",
        repo_url="https://github.mycompany.net/team-name/repo-name",
        protocol=ProtocolEnum.https,
        platform=PlatformEnum.github,
        domain="github.mycompany.net",
        owner="team-name",
        repo="repo-name",
    )
    github_enterprise_token = Case(
        origin_url="https://my_github_token@github.mycompany.net/team-name/repo-name.git",
        repo_url="https://github.mycompany.net/team-name/repo-name",
        protocol=ProtocolEnum.https,
        platform=PlatformEnum.github,
        domain="github.mycompany.net",
        owner="team-name",
        repo="repo-name",
    )
    github_enterprise_ssh = Case(
        origin_url="ssh://git@github.mycompany.net:team-name/repo-name.git",
        repo_url="https://github.mycompany.net/team-name/repo-name",
        protocol=ProtocolEnum.ssh,
        platform=PlatformEnum.github,
        domain="github.mycompany.net",
        owner="team-name",
        repo="repo-name",
    )
    github_enterprise_unknown_http = Case(
        origin_url="https://mycompany.net/team-name/repo-name.git",
        repo_url="https://mycompany.net/team-name/repo-name",
        protocol=ProtocolEnum.https,
        platform=PlatformEnum.unknown,
        domain="mycompany.net",
        owner="team-name",
        repo="repo-name",
    )
    github_enterprise_unknown_token = Case(
        origin_url="https://my_github_token@mycompany.net/team-name/repo-name.git",
        repo_url="https://mycompany.net/team-name/repo-name",
        protocol=ProtocolEnum.https,
        platform=PlatformEnum.unknown,
        domain="mycompany.net",
        owner="team-name",
        repo="repo-name",
    )
    github_enterprise_unknown_ssh = Case(
        origin_url="ssh://git@mycompany.net:team-name/repo-name.git",
        repo_url="https://mycompany.net/team-name/repo-name",
        protocol=ProtocolEnum.ssh,
        platform=PlatformEnum.unknown,
        domain="mycompany.net",
        owner="team-name",
        repo="repo-name",
    )

    # GitLab Saas
    gitlab_saas_http = Case(
        origin_url="https://gitlab.com/user-name/repo-name.git",
        repo_url="https://gitlab.com/user-name/repo-name",
        protocol=ProtocolEnum.https,
        platform=PlatformEnum.gitlab,
        domain="gitlab.com",
        owner="user-name",
        repo="repo-name",
    )
    gitlab_saas_token = Case(
        origin_url="https://oauth2:my_gitlab_token@gitlab.com/user-name/repo-name.git",
        repo_url="https://gitlab.com/user-name/repo-name",
        protocol=ProtocolEnum.https,
        platform=PlatformEnum.gitlab,
        domain="gitlab.com",
        owner="user-name",
        repo="repo-name",
    )
    gitlab_saas_ssh = Case(
        origin_url="ssh://git@gitlab.com:user-name/repo-name.git",
        repo_url="https://gitlab.com/user-name/repo-name",
        protocol=ProtocolEnum.ssh,
        platform=PlatformEnum.gitlab,
        domain="gitlab.com",
        owner="user-name",
        repo="repo-name",
    )

    # GitLab Enterprise
    gitlab_enterprise_http = Case(
        origin_url="https://my.enterprise.com/user-name/repo-name.git",
        repo_url="https://my.enterprise.com/user-name/repo-name",
        protocol=ProtocolEnum.https,
        platform=PlatformEnum.unknown,
        domain="my.enterprise.com",
        owner="user-name",
        repo="repo-name",
    )
    gitlab_enterprise_token = Case(
        origin_url="https://oauth2:my_gitlab_token@my.enterprise.com/user-name/repo-name",
        repo_url="https://my.enterprise.com/user-name/repo-name",
        protocol=ProtocolEnum.https,
        platform=PlatformEnum.unknown,
        domain="my.enterprise.com",
        owner="user-name",
        repo="repo-name",
    )
    gitlab_enterprise_ssh = Case(
        origin_url="ssh://git@my.enterprise.com:1234/user-name/repo-name.git",
        repo_url="https://my.enterprise.com/user-name/repo-name",
        protocol=ProtocolEnum.ssh,
        platform=PlatformEnum.unknown,
        domain="my.enterprise.com",
        owner="user-name",
        repo="repo-name",
    )

    # BitBucket Saas
    bitbucket_saas_http = Case(
        origin_url="https://bitbucket.org/user-name/repo-name.git",
        repo_url="https://bitbucket.org/user-name/repo-name",
        protocol=ProtocolEnum.https,
        platform=PlatformEnum.bitbucket,
        domain="bitbucket.org",
        owner="user-name",
        repo="repo-name",
    )
    bitbucket_saas_ssh = Case(
        origin_url="git@bitbucket.org:user-name/repo-name.git",
        repo_url="https://bitbucket.org/user-name/repo-name",
        protocol=ProtocolEnum.ssh,
        platform=PlatformEnum.bitbucket,
        domain="bitbucket.org",
        owner="user-name",
        repo="repo-name",
    )

    # BitBucket Enterprise
    bitbucket_enterprise_http = Case(
        origin_url="https://account-name@bitbucket.prod.mycompany.com/user-name/repo-name.git",
        repo_url="https://bitbucket.prod.mycompany.com/projects/user-name/repos/repo-name",
        protocol=ProtocolEnum.https,
        platform=PlatformEnum.bitbucket,
        domain="bitbucket.prod.mycompany.com",
        owner="user-name",
        repo="repo-name",
    )
    bitbucket_enterprise_ssh = Case(
        origin_url="ssh://git@bitbucket.prod.mycompany.com:7999/user-name/repo-name.git",
        repo_url="https://bitbucket.prod.mycompany.com/projects/user-name/repos/repo-name",
        protocol=ProtocolEnum.ssh,
        platform=PlatformEnum.bitbucket,
        domain="bitbucket.prod.mycompany.com",
        owner="user-name",
        repo="repo-name",
    )
    bitbucket_enterprise_unknown_http = Case(
        origin_url="https://account-name@prod.mycompany.com/user-name/repo-name.git",
        # note if the domain doesn't tell the platform,
        # there's no way we know the url structure should be bitbucket
        repo_url="https://prod.mycompany.com/user-name/repo-name",
        protocol=ProtocolEnum.https,
        platform=PlatformEnum.unknown,
        domain="prod.mycompany.com",
        owner="user-name",
        repo="repo-name",
    )
    bitbucket_enterprise_unknown_ssh = Case(
        origin_url="ssh://git@prod.mycompany.com:7999/user-name/repo-name.git",
        # note if the domain doesn't tell the platform,
        # there's no way we know the url structure should be bitbucket
        repo_url="https://prod.mycompany.com/user-name/repo-name",
        protocol=ProtocolEnum.ssh,
        platform=PlatformEnum.unknown,
        domain="prod.mycompany.com",
        owner="user-name",
        repo="repo-name",
    )

    # AWS CodeCommit
    aws_codecommit_http = Case(
        origin_url="https://git-codecommit.us-east-1.amazonaws.com/v1/repos/repo-name",
        repo_url="https://us-east-1.console.aws.amazon.com/codesuite/codecommit/repositories/repo-name",
        protocol=ProtocolEnum.https,
        platform=PlatformEnum.aws_codecommit,
        domain="git-codecommit.us-east-1.amazonaws.com",
        owner="",
        repo="repo-name",
    )
    aws_codecommit_ssh = Case(
        origin_url="ssh://git-codecommit.us-east-1.amazonaws.com/v1/repos/repo-name",
        repo_url="https://us-east-1.console.aws.amazon.com/codesuite/codecommit/repositories/repo-name",
        protocol=ProtocolEnum.ssh,
        platform=PlatformEnum.aws_codecommit,
        domain="git-codecommit.us-east-1.amazonaws.com",
        owner="",
        repo="repo-name",
    )
    aws_codecommit_grc = Case(
        origin_url="codecommit::us-east-1://repo-name",
        repo_url="https://us-east-1.console.aws.amazon.com/codesuite/codecommit/repositories/repo-name",
        protocol=ProtocolEnum.aws_codecommit,
        platform=PlatformEnum.aws_codecommit,
        domain="",
        owner="",
        repo="repo-name",
    )

    @classmethod
    def iter_items(cls) -> T.Iterable[T.Tuple[str, "Case"]]:
        for member in cls:
            name, case = member.name, member.value
            yield name, case
