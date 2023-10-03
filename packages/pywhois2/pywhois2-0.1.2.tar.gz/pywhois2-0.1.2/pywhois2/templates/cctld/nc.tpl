## Copyright (c) 2023 Blacknon. All rights reserved.
## Use of this source code is governed by an MIT license
## that can be found in the LICENSE file.
## =======================================================

## Macro
## =======================================================

<macro>
def str2datetime(data):
    import datetime
    import pytz
    from pytz import country_timezones

    # 登録年月日
    if 'created' in data:
        if type(data['created']) == str:
            data['created'] = datetime.datetime.fromisoformat(data['created'])

    if 'updated' in data:
        if type(data['updated']) == str:
            data['updated'] = datetime.datetime.fromisoformat(data['updated'])

    # 有効期限
    if 'expiration' in data:
        if type(data['expiration']) == str:
            data['expiration'] = datetime.datetime.strptime(
                data['expiration'].replace('+0:00', '+00:00'),
                '%Y-%m-%d'
            ).replace(tzinfo=pytz.timezone(country_timezones['nc'][0]))

    return data
</macro>

## Template
## =======================================================

OPT Whois v2.1.2

<group macro="str2datetime">
Domain                   : {{ domain_name }}
Created on               : {{ created }}
Expires on               : {{ expiration }}
Last updated on          : {{ updated }}

Domain server {{ ignore }}          : {{ name_servers | lower | ORPHRASE | to_list | joinmatches }}

Registrar                : NONE
</group>
