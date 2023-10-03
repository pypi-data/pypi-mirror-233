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
            ).replace(tzinfo=pytz.timezone(country_timezones['tm'][0]))

    # 有効期限
    if 'expiration' in data:
        if type(data['expiration']) == str:
            data['expiration'] = datetime.datetime.strptime(
                data['expiration'],
                '%Y-%m-%d'
            ).replace(tzinfo=pytz.timezone(country_timezones['tm'][0]))

    # 最終更新
    if 'updated' in data:
        if type(data['updated']) == str:
            data['updated'] = datetime.datetime.strptime(
                data['updated'],
                '%Y-%m-%d'
            ).replace(tzinfo=pytz.timezone(country_timezones['tm'][0]))

    return data
</macro>


## Template
## =======================================================

<group macro="str2datetime">
Domain : {{ domain_name | ORPHRASE }}
Status : {{ status | ORPHRASE }}
Expiry : {{ expiration | ORPHRASE }}

NS {{ ignore }}   : {{ name_servers | lower | ORPHRASE | to_list | joinmatches }}

Owner Name    : {{ registrant_name | ORPHRASE }}
Owner OrgName : {{ registrant_organization | ORPHRASE }}
Owner Addr    : {{ registrant_address | ORPHRASE | joinmatches(", ") }}
</group>
