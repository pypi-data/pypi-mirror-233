# -*- coding: utf-8 -*-

import fire
import typing as T
from pathlib import Path

from .find_web_url import get_web_url


def main(path: T.Optional[str] = None):
    if path is None:
        p = Path.cwd()
    else:
        p = Path(path)
    web_url = get_web_url(p)
    print(web_url)


def run():
    fire.Fire(main)
