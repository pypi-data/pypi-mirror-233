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
                data['created'].replace('+0:00', '+00:00'),
                '%Y-%m-%d'
            ).replace(tzinfo=pytz.timezone(country_timezones['md'][0]))

    # 有効期限
    if 'expiration' in data:
        if type(data['expiration']) == str:
            data['expiration'] = datetime.datetime.strptime(
                data['expiration'].replace('+0:00', '+00:00'),
                '%Y-%m-%d'
            ).replace(tzinfo=pytz.timezone(country_timezones['md'][0]))

    # 最終更新
    if 'updated' in data:
        if type(data['updated']) == str:
            data['updated'] = datetime.datetime.strptime(
                data['updated'].replace('+0:00', '+00:00'),
                '%Y-%m-%d'
            ).replace(tzinfo=pytz.timezone(country_timezones['md'][0]))

    return data

def status2parent(data):
    from stringcase import pascalcase, snakecase
    if 'status' in data:
        extract_data = data['status']
        if type(extract_data) == str:
            del data['status']
            data['status'] = {}
            for line in extract_data.split(","):
                data['status'][line.lstrip().lower()] = True
    return data

</macro>


## Template
## =======================================================

<group macro="str2datetime, status2parent">
Domain   name:  {{ domain_name }}
Domain  state:  {{ status | ORPHRASE }}
Registrar:      {{ registrar_name | ORPHRASE }}

Registered on:  {{ created | ORPHRASE }}
Expires    on:  {{ expiration | ORPHRASE }}

Nameserver:     {{ name_servers | ORPHRASE | to_list | joinmatches }}
</group>
