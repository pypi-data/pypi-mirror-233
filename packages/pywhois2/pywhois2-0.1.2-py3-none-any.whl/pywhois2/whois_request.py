#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2023 Blacknon. All rights reserved.
# Use of this source code is governed by an MIT license
# that can be found in the LICENSE file.
# =======================================================

import socket
import socks
from urllib import parse


# NOTE: classでやる意味なくね？？？と思ったのでfunctionにしちゃう
def whois_request(query: str, whois_host: str, proxy=""):
    """whois_request
    Args:
        query (str): _description_
        whois_host (str): _description_

    Returns:
        response (str): _description_
    """
    # 入れ物となるresponseを事前に作成しておく
    response = b''

    s = socks.socksocket(socket.AF_INET)

    if proxy != "":
        parsed_uri = parse.urlparse(proxy)
        proxy_type: socks.PROXY_TYPES
        if parsed_uri.scheme == "http":
            proxy_type = socks.PROXY_TYPE_HTTP
        elif parsed_uri.scheme == "socks4":
            proxy_type = socks.PROXY_TYPE_SOCKS4
        elif parsed_uri.scheme == "socks5":
            proxy_type = socks.PROXY_TYPE_SOCKS5

        proxy_host = parsed_uri.netloc.split(":")[0]

        s.set_proxy(proxy_type, proxy_host, parsed_uri.port)

    s.connect((whois_host, 43))
    s.send(bytes(query, 'utf-8') + b"\r\n")

    # recv returns bytes
    while True:
        d = s.recv(4096)
        response += d
        if not d:
            break

    s.close()

    response = response.decode('utf-8', 'replace')

    return response
