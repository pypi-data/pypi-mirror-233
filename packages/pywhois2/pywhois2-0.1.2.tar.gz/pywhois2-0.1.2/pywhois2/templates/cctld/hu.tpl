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
                '%Y-%m-%d %H:%M:%S'
            ).replace(tzinfo=pytz.timezone(country_timezones['hu'][0]))

    # 有効期限
    if 'expiration' in data:
        if type(data['expiration']) == str:
            data['expiration'] = datetime.datetime.strptime(
                data['expiration'],
                '%Y-%m-%d %H:%M:%S'
            ).replace(tzinfo=pytz.timezone(country_timezones['hu'][0]))

    # 最終更新
    if 'updated' in data:
        if type(data['updated']) == str:
            data['updated'] = datetime.datetime.strptime(
                data['updated'],
                '%Y-%m-%d %H:%M:%S'
            ).replace(tzinfo=pytz.timezone(country_timezones['hu'][0]))

    return data
</macro>

## Template
## =======================================================

% Whois server 3.0 serving the hu ccTLD
<group>
domain:         {{ domain_name }}
record created: {{ created | ORPHRASE }}
</group>
Tovabbi adatokert ld.:
https://www.domain.hu/domain-kereses/
For further data see:
https://www.domain.hu/domain-search/
