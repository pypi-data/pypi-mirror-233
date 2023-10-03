## Copyright (c) 2023 Blacknon. All rights reserved.
## Use of this source code is governed by an MIT license
## that can be found in the LICENSE file.
## =======================================================

## Macro
## =======================================================

<macro>
def unpack(data):
    while True:
        if type(data) == list:
            data = data[0]
        else:
            break

    update_data = {}
    for d in data:
        if type(data[d]) == list:
            if type(data[d][0]) == dict:
                data[d] = data[d][0]

        elif type(data[d]) == dict:
            if not data[d]:
                continue
        update_data[d] = data[d]
    data = update_data

    data = organization2parent('registrant', 'registrant', data)
    data = organization2parent('admin', 'admin', data)
    data = organization2parent('tech', 'tech', data)
    data = str2datetime(data)
    data = status2parent(data)

    return data

def status2parent(data):
    from stringcase import pascalcase, snakecase
    if 'status' in data:
        extract_data = data['status']
        if type(extract_data) == list:
            del data['status']
            data['status'] = {}
            for line in extract_data:
                data['status'][snakecase(line.lstrip())] = True
    return data

def organization2parent(organization_type , organization_type_name, data):
    if organization_type in data:
        if type(data[organization_type]) == dict:
            extract_data = data[organization_type]
            del data[organization_type]

            for d in extract_data:
                data["{0}_{1}".format(organization_type_name,d)] = extract_data[d]
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
                '%d.%m.%Y %H:%M:%S'
            ).replace(tzinfo=pytz.timezone(country_timezones['rs'][0]))

    # 有効期限
    if 'expiration' in data:
        if type(data['expiration']) == str:
            data['expiration'] = datetime.datetime.strptime(
                data['expiration'],
                '%d.%m.%Y %H:%M:%S'
            ).replace(tzinfo=pytz.timezone(country_timezones['rs'][0]))

    # 最終更新
    if 'updated' in data:
        if type(data['updated']) == str:
            data['updated'] = datetime.datetime.strptime(
                data['updated'],
                '%d.%m.%Y %H:%M:%S'
            ).replace(tzinfo=pytz.timezone(country_timezones['rs'][0]))

    # 最終確認
    if 'confirmed' in data:
        if type(data['confirmed']) == str:
            data['confirmed'] = datetime.datetime.strptime(
                data['confirmed'],
                '%d.%m.%Y %H:%M:%S'
            ).replace(tzinfo=pytz.timezone(country_timezones['rs'][0]))

    return data

</macro>


## Template
## =======================================================

% The data in the Whois database are provided by RNIDS
% for information purposes only and to assist persons in obtaining
% information about or related to a domain name registration record.
% Data in the database are created by registrants and we do not guarantee
% their accuracy. We reserve the right to remove access
% for entities abusing the data, without notice.
% All timestamps are given in Serbian local time.
%
<group>
Domain name: {{ domain_name }}
Domain status: {{ status | to_list | joinmatches }} {{ ignore }}
Registration date: {{ created | ORPHRASE }}
Modification date: {{ updated | ORPHRASE }}
Expiration date: {{ expiration | ORPHRASE }}
Confirmed: {{ confirmed | ORPHRASE }}
Registrar: {{ registrar_name | ORPHRASE }}

<group name="registrant">
Registrant: {{ name | ORPHRASE }}
Address: {{ address | ORPHRASE }}
Postal Code: {{ zip_code | ORPHRASE }}
ID Number: {{ id | ORPHRASE }}
Tax ID: {{ tax_id | ORPHRASE }}
</group>

<group name="admin">
Administrative contact: {{ name | ORPHRASE }}
Address: {{ address | ORPHRASE }}
Postal Code: {{ zip_code | ORPHRASE }}
ID Number: {{ id | ORPHRASE }}
Tax ID: {{ tax_id | ORPHRASE }}
</group>

<group name="tech">
Technical contact: {{ name | ORPHRASE }}
Address: {{ address | ORPHRASE }}
Postal Code: {{ zip_code | ORPHRASE }}
ID Number: {{ id | ORPHRASE }}
Tax ID: {{ tax_id | ORPHRASE }}
</group>

DNS: {{ name_servers | lower | to_list | joinmatches }} -
DNS: {{ name_servers | lower | to_list | joinmatches }} - {{ ignore | ORPHRASE }}


DNSSEC signed: {{ dnssec }}

Whois Timestamp: {{ ignore | ORPHRASE }}
</group>


<output macro="unpack" />
