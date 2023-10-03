#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2023 Blacknon. All rights reserved.
# Use of this source code is governed by an MIT license
# that can be found in the LICENSE file.
# =======================================================

# TODO: 日付をtimestamp形式で扱うよう各テンプレートで対応(macro？)
# TODO: Statusを共通の内容で処理できるよう各テンプレートで対応(macro?).
#       実装前に、最終的なdict内で扱うstatusの整理をしたほうが良いかも？なので、リリース後に調べて対応する
#       参考:
#       - https://faq.interlink.or.jp/faq2/View/wcDisplayContent.aspx?sso_step=1&id=1004

import os
import ttp
import sys

from pathlib import Path
from tld import get_tld

from .whois_request import whois_request
from .common import Message, Color, is_ipaddress, load_data_yaml, extract_domain

# CONST
TEMPLATE_DIR = "{0}/templates".format(Path(__file__).resolve().parent)


class Whois:
    TARGET = ""  # whoisでの調査対象文字列
    DATA = {}  # whoisへのrequest, parseに必要となる情報の取得
    COLOR = Color.CYAN
    IS_DEBUG = False
    PROXY = ""

    def __init__(self, target: str):
        """

        """
        target_key = ""
        if is_ipaddress(target):
            target_key = "ip_address"
        else:
            target_key = get_tld(
                target, fix_protocol=True,
                fail_silently=True
            )

        self.TARGET = target

        self.COLOR_NAME = self.COLOR + self.TARGET + Color.END
        self.MESSAGE = Message()

        if target_key is None:
            print("Error", file=sys.stderr)
            return

        # load data file
        self.DATA = load_data_yaml(target_key)

    def set_debug(self, is_debug: bool):
        """_summary_

        Args:
            is_debug (bool): _description_
        """
        self.IS_DEBUG = is_debug
        self.MESSAGE.IS_DEBUG = is_debug

    def set_proxy(self, proxy: str):
        """_summary_

        Args:
            proxy (str): _description_
        """
        self.PROXY = proxy

    def get(self):
        """

        """
        result = {}

        # tldごとのデータを取得
        server = self.DATA.get('server')
        trace_whois = self.DATA.get('trace_whois')
        strip = self.DATA.get('strip')
        templates = self.DATA.get('template')

        # serverの中身が無い場合はErrorで返す
        if server is None:
            self.MESSAGE.print_text(
                "Not found tld.",
                header=Color.RED + '[ERROR]' + Color.END,
                separator=": ",
                mode="error",
            )
            return

        self.MESSAGE.print_text(
            server,
            header=Color.CYAN + '[whois server]' + Color.END,
            separator=": ",
            mode="debug",
        )

        self.MESSAGE.print_text(
            str(trace_whois),
            header=Color.CYAN + '[is trace whois]' + Color.END,
            separator=": ",
            mode="debug",
        )

        self.MESSAGE.print_text(
            str(strip),
            header=Color.CYAN + '[strip]' + Color.END,
            separator=": ",
            mode="debug",
        )

        self.MESSAGE.print_text(
            ", ".join(templates),
            header=Color.CYAN + '[template file paths]' + Color.END,
            separator=": ",
            mode="debug",
        )

        while True:
            res = self.__get_data(server, templates, is_strip=strip)

            if 'registrar_whois_server' in res and trace_whois:
                if res['registrar_whois_server'] == server:
                    result = res
                    break

                server = res['registrar_whois_server']
                server = extract_domain(server)
                continue

            else:
                result = res
                break

        return result

    def __get_data(self, server: str, templates: list, is_strip=False):
        """

        Args:
            server (str): _description_
            templates (list): _description_

        Returns:
            _type_: _description_
        """

        result = {}

        # whois requestを実行、結果の取得
        try:
            res = "%%% start %%% {0} %%% start %%%\n".format(server)
            res += whois_request(self.TARGET, server, proxy=self.PROXY)
            res += "\n%%% end %%% {0} %%% end %%%\n".format(server)
        except Exception as e:
            print("Error: {0}".format(e), file=sys.stderr)
            return ""

        # self.is_debug次第でのlog_levelの指定
        log_level = "ERROR"
        if self.IS_DEBUG:
            log_level = "DEBUG"

        # debug messageを出力
        self.MESSAGE.print_text(
            res,
            header=Color.WHITE + '[whois response]' + Color.END,
            separator=": ",
            mode="debug",
        )

        # whoisの不要な改行を削除
        if is_strip:
            new_res_line = []
            for line in res.splitlines():
                new_line = line
                new_line = new_line.strip('\r')
                new_line = new_line.strip('\n')
                new_res_line.append(new_line)
            res = "\n".join(new_res_line)

            self.MESSAGE.print_text(
                res,
                header=Color.WHITE + '[new whois response]' + Color.END,
                separator=": ",
                mode="debug",
            )

        for t in templates:
            template_path = os.path.join(TEMPLATE_DIR, t)

            # TODO: whois_serverが含まれる場合、serverと一致しない場合は再度whoisを実行させる処理を追加する(comドメインとか向け？)
            with open(template_path, 'r') as file:
                template = file.read().rstrip()
                file.close()

            # debug messageを出力
            self.MESSAGE.print_text(
                template,
                header=Color.GREEN + '[use template]' + Color.END,
                separator=": ",
                mode="debug",
            )

            parser = ttp.ttp(res, template, log_level=log_level)
            parser.parse()
            result = parser.result(structure='flat_list')

            if any(result):
                break

        return result[0]
