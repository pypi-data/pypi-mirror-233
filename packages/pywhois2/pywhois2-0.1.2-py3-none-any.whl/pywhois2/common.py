#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2023 Blacknon. All rights reserved.
# Use of this source code is governed by an MIT license
# that can be found in the LICENSE file.
# =======================================================

import ipaddress
import yaml
import sys
import datetime

from pathlib import Path
from string import Template
from urllib.parse import urlparse

DATA_DIR = "{0}/data".format(Path(__file__).resolve().parent)


# コンソール出力時に色付をするためのClass
class Color:
    """Color

    コンソール出力時に色付をするための文字列を変数にして保持しているClass.

    Examples:
        c = Color()
        c.set(c.BLUE)
        print(c.out('hogehoge'))
    """
    # color_code
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    PURPLE = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    GRAY = '\033[1;30m'

    # 文字効果
    BOLD = '\038[1m'
    ITALIC = '\038[3m'
    UNDERLINE = '\033[4m'
    INVISIBLE = '\033[08m'
    REVERCE = '\033[07m'

    # 効果を終了
    END = '\033[0m'

    def __init__(self, color_code: str):
        """[summary]

        Args:
            color_code (str): 使用するカラーコード

        """
        self.COLOR_CODE = color_code

    def out(self, text: str, is_bold=False, is_underline=False, is_reverse=False, is_italic=False):
        # textを囲む
        text = self.COLOR_CODE + text + self.END

        # is_boldが有効な場合、太字にする
        if is_bold:
            text = self.BOLD + text + self.END

        # is_underlineが有効な場合、下線を入れる
        if is_underline:
            text = self.UNDERLINE + text + self.END

        # is_reverseが有効な場合、色の反転をする
        if is_reverse:
            text = self.REVERCE + text + self.END

        # is_italicが有効な場合、Italicにする
        if is_italic:
            text = self.ITALIC + text + self.END

        return text


# Message関連の制御用Class
class Message:
    """Message

    メッセージの出力を簡易化するためのClass.

    Examples:
    """

    def __init__(self):
        # command flag
        self.IS_COMMAND = False

        # debug flag
        self.IS_DEBUG = False

        # timestamp flag
        self.IS_TIMESTAMP = False

        # engine data
        self.ENGINE_COLOR = Color('')
        self.ENGINE_NAME = ''
        self.ENGINE = ''

        # header
        self.HEADER = ''

    def set_is_command(self, is_command: bool):
        self.IS_COMMAND = is_command

    def set_is_debug(self, is_debug: bool):
        self.IS_DEBUG = is_debug

    def set_engine(self, engine: str, color: str):
        self.ENGINE_COLOR = Color(color)
        self.ENGINE_NAME = engine
        self.ENGINE = self.ENGINE_COLOR.out(engine)

    def set_header(self, text):
        self.HEADER = text

    def replace(self, text):
        """replace

        テンプレートテキストの変数をself変数や時刻に置換して返す

        Args:
            text (str): 置換処理をするテンプレート用テキスト
        """

        # 現在時刻を取得
        dt_now = datetime.datetime.now()

        # 置換用のdictを生成
        data = {
            # 時刻情報
            'YEAR': dt_now.year,
            'MONTH': dt_now.month,
            'DAY': dt_now.day,
            'HOUR': dt_now.hour,
            'MINUTE': dt_now.minute,
            'SECOND': dt_now.second,

            # 検索エンジン(color)
            'ENGINE': self.ENGINE,  # 色付き
            'ENGINE_NAME': self.ENGINE_NAME,  # 色なし
        }

        # テンプレートを作成
        template = Template(text)

        # 置換処理を実行
        result = template.safe_substitute(data)

        return result

    def print_line(self, *text, use_header=True, separator=' ', file=sys.stdout, header=None):
        """print_line

        メッセージを出力する(行)

        Args:
            text: メッセージとして出力するテキスト行
            use_header: `header`で指定しているヘッダーを行頭に表示するかどうか
            separator: printする際に使用する区切り文字
            file: 出力先のファイル(デフォルトはstdout)
            header: ヘッダーとして使用する文字列を指定
        """
        # headerの生成
        if header is None:
            header = self.HEADER

        header = self.replace(header)

        # テキストを出力
        if use_header:
            print(header, *text, sep=separator, file=file)
        else:
            print(*text, sep=separator, file=file)

    def print_text(self, text, mode='message', use_header=True, separator=' ', file=sys.stdout, header=None):
        """print_line

        メッセージを出力する(テキスト)

        Args:
            text: メッセージとして出力するテキスト
            mode: メッセージの出力モード(`message`, `error`, `warn`, `info`, `debug`)
            use_header: `header`で指定しているヘッダーを行頭に表示するかどうか
            separator: printする際に使用する区切り文字
            file: 出力先のファイル(デフォルトはstdout)
            header: ヘッダーとして使用する文字列を指定
        """
        # is_commandが有効のときのみ出力させる
        if not self.IS_COMMAND:
            return

        # debug, infoのときは、self.is_debugが有効のときのみ出力
        if mode in ('info', 'debug'):
            # self.is_debugでない場合は出力しない
            if not self.IS_DEBUG:
                return

        # 出力テキストの生成
        text = self.replace(text)

        # case
        text_color = Color(Color.END)
        if mode == 'message':  # modeが `message` のとき
            text_color = Color(Color.WHITE)

        elif mode == 'error':
            text_color = Color(Color.RED)
            file = sys.stderr

        elif mode == 'warn':
            text_color = Color(Color.YELLOW)
            file = sys.stderr

        elif mode == 'info':
            text_color = Color(Color.GREEN)
            file = sys.stderr

        elif mode == 'debug':
            text_color = Color(Color.GRAY)
            file = sys.stderr

        # default headerの定義
        if mode in ('info', 'debug'):
            if header is None:
                header = self.HEADER

            header = Color.REVERCE + \
                self.replace(header) + Color.END

        # TODO: 正規表現で、付きの箇所を抜き出すような処理を追加で入れる

        # テキストの出力
        for line in text.splitlines():
            self.print_line(text_color.out(line),
                            separator=separator, use_header=use_header, file=file, header=header)

        return


def is_ipaddress(host: str):
    """_summary_

    Args:
        host (str): _description_

    Returns:
        _type_: _description_
    """
    try:
        ipaddress.ip_address(host)
        return True
    except Exception:
        return False


def load_data_yaml(target_key: str, yaml_path_list: list = []):
    """

    Args:
        path (str): _description_
    """
    result = {}

    # target_key to  list
    key_candidate = []
    key_elements = target_key.split(".")
    joined_key = ""
    for i in reversed(range(len(key_elements) * -1, 0)):
        if joined_key == "":
            joined_key = key_elements[i]
        else:
            joined_key = "{0}.{1}".format(key_elements[i], joined_key)
        key_candidate.append(joined_key)

    # tld候補のリストを逆順にする
    key_candidate.reverse()

    if len(yaml_path_list) == 0:
        yaml_path_list = [
            "{0}/{1}".format(DATA_DIR, "data.yml"),
            "{0}/{1}".format(DATA_DIR, "gtld.yml"),
            "{0}/{1}".format(DATA_DIR, "cctld.yml"),
        ]

    obj = {}
    for yaml_path in yaml_path_list:
        with open(yaml_path) as file:
            # load data
            obj.update(yaml.safe_load(file))

    # get common
    common_data = obj.get('common')

    # get key loops
    res = {}
    for k in key_candidate:
        if k in obj:
            res = obj.get(k)
            break

    # `.no`など、先頭にdotがついているものも対象とさせる(ただし優先度は低くする)
    if len(res) == 0:
        for k in key_candidate:
            if ".{0}".format(k) in obj:
                res = obj.get(".{0}".format(k))
                break

    if len(res) == 0:
        res = common_data

    # server, templateがないdataについてはcommonの内容に上書きさせる
    result = dict(common_data, **res)

    return result


def extract_domain(text: str):
    result = ""
    is_url = False

    try:
        r = urlparse(text)
        is_url = all([r.scheme, r.netloc])
    except Exception:
        is_url = False

    if is_url:
        parsed_url = urlparse(text)
        result = parsed_url.netloc
    else:
        result = text
        result.rstrip("/")

    return result


def json_serial(obj):
    # 日付型の場合には、文字列に変換します
    if isinstance(obj, (datetime.datetime, datetime.date)):
        return obj.strftime("%Y/%m/%d %H:%M:%S %z")
        # return obj.isoformat()
    # 上記以外はサポート対象外.
    raise TypeError("Type %s not serializable" % type(obj))
