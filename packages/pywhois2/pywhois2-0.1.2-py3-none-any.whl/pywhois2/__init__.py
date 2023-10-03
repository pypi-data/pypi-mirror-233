#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2023 Blacknon. All rights reserved.
# Use of this source code is governed by an MIT license
# that can be found in the LICENSE file.
# =======================================================

import json

import argparse
from argparse import RawTextHelpFormatter

from pkg_resources import get_distribution

# from .whois_request import whois_request
from .whois import Whois
from .common import json_serial

# version (setup.pyから取得してくる)
__version__ = get_distribution('pydork').version


def main():
    # parserの作成
    help_text = 'whois parser command.'
    parser = argparse.ArgumentParser(
        description=help_text,
        formatter_class=RawTextHelpFormatter,
    )

    # TODO: 複数取得可能にする
    parser.add_argument(
        "target", action="store", type=str, help=""
    )

    parser.add_argument(
        "--debug", action="store_true", help=""
    )

    parser.add_argument(
        "--proxy", "-P", default="",
        type=str, help=""
    )

    # TODO: 出力フォーマットを指定可能にする

    # args
    args = parser.parse_args()

    whois = Whois(args.target)
    whois.MESSAGE.set_is_command(True)

    whois.set_debug(args.debug)
    whois.set_proxy(args.proxy)
    result = whois.get()

    print(json.dumps(result, default=json_serial))


if __name__ == '__main__':
    main()
