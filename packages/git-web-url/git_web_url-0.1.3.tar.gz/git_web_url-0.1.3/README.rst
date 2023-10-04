
.. .. image:: https://readthedocs.org/projects/git-web-url/badge/?version=latest
    :target: https://git-web-url.readthedocs.io/en/latest/
    :alt: Documentation Status

.. image:: https://github.com/MacHu-GWU/git_web_url-project/workflows/CI/badge.svg
    :target: https://github.com/MacHu-GWU/git_web_url-project/actions?query=workflow:CI

.. image:: https://codecov.io/gh/MacHu-GWU/git_web_url-project/branch/main/graph/badge.svg
    :target: https://codecov.io/gh/MacHu-GWU/git_web_url-project

.. image:: https://img.shields.io/pypi/v/git-web-url.svg
    :target: https://pypi.python.org/pypi/git-web-url

.. image:: https://img.shields.io/pypi/l/git-web-url.svg
    :target: https://pypi.python.org/pypi/git-web-url

.. image:: https://img.shields.io/pypi/pyversions/git-web-url.svg
    :target: https://pypi.python.org/pypi/git-web-url

.. image:: https://img.shields.io/badge/Release_History!--None.svg?style=social
    :target: https://github.com/MacHu-GWU/git_web_url-project/blob/main/release-history.rst

.. image:: https://img.shields.io/badge/STAR_Me_on_GitHub!--None.svg?style=social
    :target: https://github.com/MacHu-GWU/git_web_url-project

------

.. .. image:: https://img.shields.io/badge/Link-Document-blue.svg
    :target: https://git-web-url.readthedocs.io/en/latest/

.. .. image:: https://img.shields.io/badge/Link-API-blue.svg
    :target: https://git-web-url.readthedocs.io/en/latest/py-modindex.html

.. image:: https://img.shields.io/badge/Link-Install-blue.svg
    :target: `install`_

.. image:: https://img.shields.io/badge/Link-GitHub-blue.svg
    :target: https://github.com/MacHu-GWU/git_web_url-project

.. image:: https://img.shields.io/badge/Link-Submit_Issue-blue.svg
    :target: https://github.com/MacHu-GWU/git_web_url-project/issues

.. image:: https://img.shields.io/badge/Link-Request_Feature-blue.svg
    :target: https://github.com/MacHu-GWU/git_web_url-project/issues

.. image:: https://img.shields.io/badge/Link-Download-blue.svg
    :target: https://pypi.org/pypi/git-web-url#files


Welcome to ``git_web_url`` Documentation
==============================================================================
``git_web_url`` is a CLI tool and also a Python library can print the url of a local file in a git repo so you can one-click to open it in web browser.

Currently it supports:

- GitHub
- GitHub Enterprise
- GitLab
- GitLab Enterprise
- BitBucket
- BitBucket Enterprise
- AWS CodeCommit

**Usage Example**

1. **Auto-discover the git repo**:

cd into your git repo directory, or any folder inside, then run ``gwu``, it prints the url for the current branch and the current directory:

.. code-block:: bash

    $ gwu # or gitweburl
    https://github.com/your_account/your_repo/tree/your_branch/path/to/current_directory


2. **Explicitly specify the file or folder**:

copy the absolute path of the file or folder in your local git repo, then run ``gwu ${absolute_path_here}``:

.. code-block:: bash

    $ gwu /Users/myusername/GitHub/your_repo/path/to/your_file
    https://github.com/your_account/your_repo/tree/your_branch/path/to/current_directory


.. _install:

Install
------------------------------------------------------------------------------

``git_web_url`` is released on PyPI, so all you need is to:

.. code-block:: console

    $ pip install git-web-url

To upgrade to latest version:

.. code-block:: console

    $ pip install --upgrade git-web-url
