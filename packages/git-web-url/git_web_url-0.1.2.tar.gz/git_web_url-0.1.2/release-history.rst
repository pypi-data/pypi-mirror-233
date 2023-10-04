.. _release_history:

Release and Version History
==============================================================================


x.y.z (Backlog)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

**Minor Improvements**

**Bugfixes**

**Miscellaneous**


0.1.2 (2023-10-03)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Bugfixes**

- Fix a bug that cannot detect the git repo dir when you are already at the git repo dir.

**Miscellaneous**

- Add CLI help info.


0.1.1 (2023-10-03)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- First release.
- Add support for AWS CodeCommit, BitBucket, BitBucket Enterprise, GitHub, GitHub Enterprise, GitLab, GitLab Enterprise.
- Add the following public API:
    - ``git_web_url.api.PlatformEnum``
    - ``git_web_url.api.ProtocolEnum``
    - ``git_web_url.api.get_web_url``
- Add the CLI command ``gitweburl`` or ``gwu``.
