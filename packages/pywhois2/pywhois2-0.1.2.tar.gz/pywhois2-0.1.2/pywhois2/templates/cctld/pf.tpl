## Copyright (c) 2023 Blacknon. All rights reserved.
## Use of this source code is governed by an MIT license
## that can be found in the LICENSE file.
## =======================================================

## Macro
## =======================================================

<macro>
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

def str2datetime(data):
    import datetime
    import pytz
    from pytz import country_timezones

    # 登録年月日
    if 'created' in data:
        if type(data['created']) == str:
            data['created'] = datetime.datetime.strptime(
                data['created'].replace('+0:00', '+00:00'),
                '%d/%m/%Y'
            ).replace(tzinfo=pytz.timezone(country_timezones['pf'][0]))

    # 有効期限
    if 'expiration' in data:
        if type(data['expiration']) == str:
            data['expiration'] = datetime.datetime.strptime(
                data['expiration'].replace('+0:00', '+00:00'),
                '%d/%m/%Y'
            ).replace(tzinfo=pytz.timezone(country_timezones['pf'][0]))

    # 最終更新
    if 'updated' in data:
        if type(data['updated']) == str:
            data['updated'] = datetime.datetime.strptime(
                data['updated'].replace('+0:00', '+00:00'),
                '%d/%m/%Y'
            ).replace(tzinfo=pytz.timezone(country_timezones['pf'][0]))

    return data
</macro>

## Template
## =======================================================

This is the PF top level domain whois server.
<group macro="str2datetime, status2parent">
Informations about '{{ domain_name }}' :

Status : {{ status }}
Created (JJ/MM/AAAA) : {{ created | ORPHRASE }}
Last renewed (JJ/MM/AAAA) : {{ updated | ORPHRASE }}
Expire (JJ/MM/AAAA) : {{ expiration | ORPHRASE }}
Name server {{ ignore }} : {{ name_servers | lower | ORPHRASE | to_list | joinmatches }}
Registrant Company Name : {{ registrant_organization | ORPHRASE }}
Registrant Name : {{ registrant_name | ORPHRASE }}
Registrant Address : {{ registrant_address | ORPHRASE | joinmatches(", ") }}
Registrant Postal Code : {{ registrant_zip_code }}
Registrant City :  {{ registrant_address | ORPHRASE | joinmatches(", ") }}
Registrant Country :  {{ registrant_country | ORPHRASE }}
Tech {{ ignore }} Company Name : {{ tech_organization | ORPHRASE }}
Tech {{ ignore }} Name : {{ tech_name }}
Tech {{ ignore }} Address : {{ tech_address | ORPHRASE | joinmatches(", ") }}
Tech {{ ignore }} Postal Code : {{ tech_zip_code }}
Tech {{ ignore }} City : {{ tech_address | ORPHRASE | joinmatches(", ") }}
Tech {{ ignore }} Country : {{ tech_country | ORPHRASE }}
Registrar Company Name :  {{ registrar_name | ORPHRASE }}
Registrar Address : {{ registrar_address | ORPHRASE | joinmatches(", ") }}
Registrar Postal Code : {{ registrar_zip_code }}
Registrar City : {{ registrar_address | ORPHRASE | joinmatches(", ") }}
Registrar Country : {{ registrar_country | ORPHRASE }}
</group>
