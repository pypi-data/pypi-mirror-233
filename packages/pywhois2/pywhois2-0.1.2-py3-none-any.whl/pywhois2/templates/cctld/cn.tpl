## Copyright (c) 2023 Blacknon. All rights reserved.
## Use of this source code is governed by an MIT license
## that can be found in the LICENSE file.
## =======================================================

## Macro
## =======================================================

<macro>
def standardize_status(data):
    from stringcase import pascalcase, snakecase
    if 'status' in data:
        if type(data['status']) == list:
            extract_data = data['status']
            del data['status']
            data['status'] = {}

            for d in extract_data:
                data['status'][snakecase(d.lstrip())] = True

    return data

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
            ).replace(tzinfo=pytz.timezone(country_timezones['cn'][0]))

    # 有効期限
    if 'expiration' in data:
        if type(data['expiration']) == str:
            data['expiration'] = datetime.datetime.strptime(
                data['expiration'],
                '%Y-%m-%d %H:%M:%S'
            ).replace(tzinfo=pytz.timezone(country_timezones['cn'][0]))

    # 最終更新
    if 'updated' in data:
        if type(data['updated']) == str:
            data['updated'] = datetime.datetime.strptime(
                data['updated'],
                '%Y-%m-%d %H:%M:%S'
            ).replace(tzinfo=pytz.timezone(country_timezones['cn'][0]))

    return data

</macro>


## Template
## =======================================================

<group macro="standardize_status, str2datetime">
Domain Name: {{ domain_name | lower | ORPHRASE }}
ROID: {{ domain_roid | ORPHRASE }}
Domain Status: {{ status | ORPHRASE | to_list | joinmatches }}
Registrant: {{ registrant_name | ORPHRASE }}
Registrant Contact Email: {{ registrant_email | ORPHRASE }}
Sponsoring Registrar: {{ registrar_name | ORPHRASE }}
Name Server: {{ name_servers | ORPHRASE | to_list | joinmatches }}
Registration Time: {{ created | ORPHRASE }}
Expiration Time: {{ expiration | ORPHRASE }}
DNSSEC: {{ dnssec | ORPHRASE }}
</group>
