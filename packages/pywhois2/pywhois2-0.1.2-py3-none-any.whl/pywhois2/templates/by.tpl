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
            data['created'] = datetime.datetime.strptime(
                data['created'],
                '%Y-%m-%d'
            ).replace(tzinfo=pytz.timezone(country_timezones['by'][0]))

    # 有効期限
    if 'expiration' in data:
        if type(data['expiration']) == str:
            data['expiration'] = datetime.datetime.strptime(
                data['expiration'],
                '%Y-%m-%d'
            ).replace(tzinfo=pytz.timezone(country_timezones['by'][0]))

    # 最終更新
    if 'updated' in data:
        if type(data['updated']) == str:
            data['updated'] = datetime.datetime.strptime(
                data['updated'],
                '%Y-%m-%d'
            ).replace(tzinfo=pytz.timezone(country_timezones['by'][0]))

    return data
</macro>

## Template
## =======================================================

<group macro="str2datetime" del="_ignore_">
%%% start %%% {{ _ignore_ }} %%% start %%%
Domain Name: {{ domain_name | lower | ORPHRASE }}

Registrar: {{ registrar_name | ORPHRASE }}

Org: {{ registrant_organization | ORPHRASE }}
Country: {{ registrant_country }}
Address: {{ registrant_address | ORPHRASE }}
Registration or other identification number: {{ registrant_id }}
Phone: {{ registrant_phone }}
Email: {{ registrant_email }}

Name Server: {{ name_servers | lower | ORPHRASE | to_list | joinmatches }}
Update Date: {{ updated | ORPHRASE }}
Creation Date: {{ created | ORPHRASE }}
Expiration Date: {{ expiration | ORPHRASE }}
</group>
