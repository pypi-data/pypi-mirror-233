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

    data = status2parent(data)
    data = organization2parent('registrant', 'registrant', data)
    data = organization2parent('tech', 'tech', data)
    data = name_servers2parent(data)
    data = str2datetime(data)

    return data

def update_line(data):
    if 'line' in data:
        extract_data = data['line']
        del data['line']

        data['name'] = extract_data[0]
        if len(extract_data) == 5:
            data['organization'] = extract_data[1]
            data['address'] = ", ".join(extract_data[2:-2])
            data['country'] = ", ".join(extract_data[-1])
        else:
            data['address'] = ", ".join(extract_data[1:-2])
            data['country'] = ", ".join(extract_data[-1])
    return data

def status2parent(data):
    from stringcase import pascalcase, snakecase
    if 'status' in data:
        extract_data = data['status']
        if type(extract_data) == list:
            del data['status']
            data['status'] = {}
            for line in extract_data:
                data['status'][line.lstrip().lower().replace(' ', '_')] = True
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

def str2datetime(data):
    import datetime
    import pytz
    from pytz import country_timezones

    # 登録年月日
    if 'created' in data:
        if type(data['created']) == str:
            data['created'] = datetime.datetime.strptime(
                data['created'],
                '%d/%m/%Y'
            ).replace(tzinfo=pytz.timezone(country_timezones['sm'][0]))

    # 有効期限
    if 'expiration' in data:
        if type(data['expiration']) == str:
            data['expiration'] = datetime.datetime.strptime(
                data['expiration'],
                '%d/%m/%Y'
            ).replace(tzinfo=pytz.timezone(country_timezones['sm'][0]))

    # 最終更新
    if 'updated' in data:
        if type(data['updated']) == str:
            data['updated'] = datetime.datetime.strptime(
                data['updated'],
                '%d/%m/%Y'
            ).replace(tzinfo=pytz.timezone(country_timezones['sm'][0]))

    return data

</macro>


## Template
## =======================================================

<group>
Domain Name: {{ domain_name }}
Registration date: {{ created | ORPHRASE }}
Status: {{ status }}

<group name="registrant" macro="update_line">
Owner:{{ _start_ }}
{{ line | _line_ | to_list | joinmatches }}
Phone: {{ phone }}
Fax: {{ fax }}
Email: {{ email }}
{{ _end_ }}
</group>

<group name="tech" macro="update_line">
Technical Contact:{{ _start_ }}
{{ line | _line_ | to_list | joinmatches }}
Phone: {{ phone }}
Fax: {{ fax }}
Email: {{ email }}
{{ _end_ }}
</group>

<group name="name_servers">
DNS Servers:{{ _start_ }}
{{ name_servers | lower | ORPHRASE | to_list | joinmatches }}
{{ _end_ }}
</group>
</group>

<output macro="unpack" />
