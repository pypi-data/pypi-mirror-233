## Copyright (c) 2023 Blacknon. All rights reserved.
## Use of this source code is governed by an MIT license
## that can be found in the LICENSE file.
## =======================================================

## Macro
## =======================================================

<macro>
def delete_empty_line(data):
    new_data = []
    group_header_line = [
        'Name servers in the listed order:'
    ]

    before_line = ''
    for line in data.splitlines():
        if not before_line in group_header_line:
            new_data.append(line)
        before_line = line
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

    data = organization2parent('administrative', 'admin', data)
    data = organization2parent('technical', 'tech', data)
    data = organization2parent('billing', 'billing', data)
    data = name_servers2parent(data)
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
        extract_data = data['name_servers']
        if type(extract_data) == dict:
            del data['name_servers']
            data['name_servers'] = []
            for line in extract_data['name_servers']:
                data['name_servers'].append(line.split(" ")[0].lower())
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
                '%a %b %d %H:%M:%S %Y'
            ).replace(tzinfo=pytz.timezone(country_timezones['kg'][0]))

    # 有効期限
    if 'expiration' in data:
        if type(data['expiration']) == str:
            data['expiration'] = datetime.datetime.strptime(
                data['expiration'],
                '%a %b %d %H:%M:%S %Y'
            ).replace(tzinfo=pytz.timezone(country_timezones['kg'][0]))

    # 最終更新
    if 'updated' in data:
        if type(data['updated']) == str:
            data['updated'] = datetime.datetime.strptime(
                data['updated'],
                '%a %b %d %H:%M:%S %Y'
            ).replace(tzinfo=pytz.timezone(country_timezones['kg'][0]))

    return data
</macro>


## Template
## =======================================================

<input macro="delete_empty_line" />


% This is the .kg ccTLD Whois server
% Register your own domain at http://www.cctld.kg
% Use @cctld_kg_bot telegram bot for whois service

<group>
Domain {{ domain_name | lower }} ({{ status | lower }})

<group name="{{ group_type }}" >
{{ group_type | lower }} Contact:
   PID: {{ pid }}
   Name: {{ organization | ORPHRASE }}
   Address: {{ address | ORPHRASE }}
   Email: {{ email | ORPHRASE }}
   phone: {{ phone | ORPHRASE }}
   fax: {{ fax | ORPHRASE }}
</group>


Record created: {{ created | ORPHRASE }}
Record last updated on:  {{ updated | ORPHRASE }}
Record expires on: {{ expiration | ORPHRASE }}

<group name="name_servers">
Name servers in the listed order:{{ _start_ }}
{{ name_servers | ORPHRASE | to_list | joinmatches }}
{{ _end_ }}
</group>

</group>

<output macro="unpack" />
