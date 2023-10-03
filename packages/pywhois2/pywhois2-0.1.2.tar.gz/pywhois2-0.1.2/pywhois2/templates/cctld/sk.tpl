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
    data = organization2parent('registrar', 'registrar', data)
    data = organization2parent('admin', 'admin', data)
    data = organization2parent('tech', 'tech', data)
    data = str2datetime(data)

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
                '%Y-%m-%d'
            ).replace(tzinfo=pytz.timezone(country_timezones['sk'][0]))

    # 有効期限
    if 'expiration' in data:
        if type(data['expiration']) == str:
            data['expiration'] = datetime.datetime.strptime(
                data['expiration'],
                '%Y-%m-%d'
            ).replace(tzinfo=pytz.timezone(country_timezones['sk'][0]))

    # 最終更新
    if 'updated' in data:
        if type(data['updated']) == str:
            data['updated'] = datetime.datetime.strptime(
                data['updated'],
                '%Y-%m-%d'
            ).replace(tzinfo=pytz.timezone(country_timezones['sk'][0]))

    return data
</macro>


## Template
## =======================================================

<group>
Domain:                       {{ domain_name }}
Created:                      {{ created | ORPHRASE }}
Valid Until:                  {{ expiration | ORPHRASE }}
Updated:                      {{ updated | ORPHRASE }}
Domain Status:                {{ status }}
Nameserver:                   {{ name_servers | lower | ORPHRASE | to_list | joinmatches }}
DNSSEC:                       {{ dnssec }}

<group name="registrant" macro="str2datetime">
{{ _start_ }}
Domain registrant:            {{ id }}
Name:                         {{ name | ORPHRASE }}
Organization:                 {{ organization | ORPHRASE }}
Organization ID:              {{ organization_id }}
Street:                       {{ address | ORPHRASE | joinmatches(", ") }}
City:                         {{ address | ORPHRASE | joinmatches(", ") }}
Postal Code:                  {{ zip_code | ORPHRASE }}
Country Code:                 {{ country | ORPHRASE }}
Authorised Registrar:         {{ registrar_id }}
Created:                      {{ created }}
Updated:                      {{ updated }}
{{ _end_ }}
</group>

<group name="registrar" macro="str2datetime">
Registrar:                    {{ id }}
Name:                         {{ name | ORPHRASE }}
Organization:                 {{ organization | ORPHRASE }}
Organization ID:              {{ organization_id }}
Phone:                        {{ phone }}
Email:                        {{ email }}
Street:                       {{ address | ORPHRASE | joinmatches(", ") }}
City:                         {{ address | ORPHRASE | joinmatches(", ") }}
Postal Code:                  {{ zip_code | ORPHRASE }}
Country Code:                 {{ country | ORPHRASE }}
Created:                      {{ created }}
Updated:                      {{ updated }}
</group>

<group name="admin" macro="str2datetime">
Administrative Contact:       {{ id }}
Name:                         {{ name | ORPHRASE }}
Organization:                 {{ organization | ORPHRASE }}
Organization ID:              {{ organization_id }}
Phone:                        {{ phone }}
Email:                        {{ email }}
Street:                       {{ address | ORPHRASE | joinmatches(", ") }}
City:                         {{ address | ORPHRASE | joinmatches(", ") }}
Postal Code:                  {{ zip_code | ORPHRASE }}
Country Code:                 {{ country | ORPHRASE }}
Created:                      {{ created }}
Updated:                      {{ updated }}
</group>

<group name="tech" macro="str2datetime">
Technical Contact:            {{ id }}
Name:                         {{ name | ORPHRASE }}
Organization:                 {{ organization | ORPHRASE }}
Organization ID:              {{ organization_id }}
Phone:                        {{ phone }}
Email:                        {{ email }}
Street:                       {{ address | ORPHRASE | joinmatches(", ") }}
City:                         {{ address | ORPHRASE | joinmatches(", ") }}
Postal Code:                  {{ zip_code | ORPHRASE }}
Country Code:                 {{ country | ORPHRASE }}
Created:                      {{ created }}
Updated:                      {{ updated }}
</group>
</group>

<output macro="unpack" />
