## Copyright (c) 2023 Blacknon. All rights reserved.
## Use of this source code is governed by an MIT license
## that can be found in the LICENSE file.
## =======================================================

## Macro
## =======================================================

<macro>
def add_empty_line(data):
    new_data = []
    group_header_line = [
        'Address',
        'Tel',
    ]

    for line in data.splitlines():
        xline = line.split(":......")[0]
        if xline in group_header_line:
            new_data.append("")
        new_data.append(line)
    data = "\n".join(new_data)

    return data

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

    data = common2parent(data)
    data = status2parent(data)
    data = str2datetime(data)
    data = organization2parent('owner', 'registrant', data)
    data = organization2parent('administrative', 'admin', data)
    data = organization2parent('technical', 'tech', data)

    return data

def address2parent(data):
    if 'address' in data:
        if type(data['address']) == list:
            data['address'] = data['address'][0]['address']
    return data

def organization2parent(organization_type , organization_type_name, data):
    if organization_type in data:
        if type(data[organization_type]) == dict:
            extract_data = data[organization_type]
            del data[organization_type]

            for d in extract_data:
                data["{0}_{1}".format(organization_type_name,d)] = extract_data[d]
    return data

def common2parent(data):
    new_data = {}
    for d in data:
        if 'domain_name' in data[d]:
            if 'domain_name' not in new_data:
                new_data['domain_name'] = data[d]['domain_name']
            del data[d]['domain_name']

        if 'status' in data[d]:
            if 'status' not in new_data:
                new_data['status'] = data[d]['status']
            del data[d]['status']

        if 'expiration' in data[d]:
            if 'expiration' not in new_data:
                new_data['expiration'] = data[d]['expiration']
            del data[d]['expiration']

        if 'created' in data[d]:
            if 'created' not in new_data:
                new_data['created'] = data[d]['created']
            del data[d]['created']

        if 'name_servers' in data[d]:
            if 'name_servers' not in new_data:
                new_data['name_servers'] = data[d]['name_servers']
            del data[d]['name_servers']

        new_data[d] = data[d]

    data = new_data

    return data

def status2parent(data):
    from stringcase import pascalcase, snakecase
    import re
    if 'status' in data:
        extract_data = data['status']
        if type(extract_data) == str:
            del data['status']
            data['status'] = {}

            for line in extract_data.split(' '):
                if re.match("Activ.+", line):
                    line = 'active'
                data['status'][snakecase(line.lstrip())] = True
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
            ).replace(tzinfo=pytz.timezone(country_timezones['tg'][0]))

    # 有効期限
    if 'expiration' in data:
        if type(data['expiration']) == str:
            data['expiration'] = datetime.datetime.strptime(
                data['expiration'],
                '%Y-%m-%d'
            ).replace(tzinfo=pytz.timezone(country_timezones['tg'][0]))

    # 最終更新
    if 'updated' in data:
        if type(data['updated']) == str:
            data['updated'] = datetime.datetime.strptime(
                data['updated'],
                '%Y-%m-%d'
            ).replace(tzinfo=pytz.timezone(country_timezones['tg'][0]))

    return data
</macro>

## Template
## =======================================================

<input macro="add_empty_line" />

This is JWhoisServer serving ccTLD tg
Java Whois Server 0.4.1.3    (c) 2006 - 2015 Klaus Zerwes zero-sys.net
All rights reserved.
Copyright "NICTogo2 - http://www.nic.tg"

<group name="{{ contact_type }}" macro="address2parent">
Domain:.............{{ domain_name }}
Registrar:..........{{ registrar_name | ORPHRASE }}
Activation:.........{{ created | ORPHRASE }}
Expiration:.........{{ expiration | ORPHRASE }}
Status:.............{{ status }}
Contact Type:.......{{ contact_type | ORPHRASE }}
Last Name:..........{{ name | ORPHRASE | joinmatches(" ") }}
First Name:.........{{ name | ORPHRASE | joinmatches(" ") }}

<group name="address">
{{ _start_ }}
Address:............{{ address | ORPHRASE | joinmatches(" ") }}
{{ address | joinmatches(", ") }}
{{ _end_ }}
</group>

Tel:................{{ phone | ORPHRASE }}
Fax:................{{ fax | ORPHRASE }}
e-mail:.............{{ email | ORPHRASE }}
Name Server (DB):...{{ name_servers | lower | ORPHRASE | to_list | joinmatches }}
</group>

----------------------------------------


<output macro="unpack" />
