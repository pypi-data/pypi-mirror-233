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

    data = organization2parent('registrar', 'registrar', data)
    data = name_servers2parent(data)
    data = domain_name2parent(data)
    data = date2parent(data)
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

def name_servers2parent(data):
    if 'name_servers' in data:
        extract_data = data['name_servers']['name_servers']
        if type(extract_data) == list:
            del data['name_servers']
            data['name_servers'] = extract_data

    return data

def domain_name2parent(data):
    if 'domain_name' in data:
        extract_data = data['domain_name']['domain_name']
        if type(extract_data) == str:
            del data['domain_name']
            data['domain_name'] = extract_data

    return data

def date2parent(data):
    if 'date' in data:
        if type(data['date']) == dict:
            extract_data = data['date']
            del data['date']

            for d in extract_data:
                data[d] = extract_data[d]
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
                '%d-%b-%Y'
            ).replace(tzinfo=pytz.timezone("GMT"))

    # 有効期限
    if 'expiration' in data:
        if type(data['expiration']) == str:
            data['expiration'] = datetime.datetime.strptime(
                data['expiration'],
                '%d-%b-%Y'
            ).replace(tzinfo=pytz.timezone("GMT"))

    # 最終更新
    if 'updated' in data:
        if type(data['updated']) == str:
            data['updated'] = datetime.datetime.strptime(
                data['updated'],
                '%d-%b-%Y'
            ).replace(tzinfo=pytz.timezone("GMT"))

    return data


</macro>

## Template
## =======================================================

<group>
<group name="domain_name">
    Domain name:{{ _start_ }}
        {{ domain_name }}
</group>

    Data validation:
        Nominet was able to match the registrant's name and address against a 3rd party data source on {{ ignore }}

<group name="registrar">
    Registrar:
        {{ registrar_name | ORPHRASE }} [Tag = {{ registrar_id }}]
        URL: {{ registrar_url }}
</group>

<group name="date">
    Relevant dates:
        Registered on: {{ created }}
        Expiry date:  {{ expiration }}
        Last updated:  {{ updated }}
</group>

    Registration status:
        Registered until {{ ignore }} date.

<group name="name_servers">
    Name servers:{{ _start_ }}
        {{ name_servers | ORPHRASE | to_list | joinmatches }}
{{ _end_ }}
</group>

    WHOIS lookup made at {{ ignore }}
</group>

<output macro="unpack" />
