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
        update_data[d] = data[d]
    data = update_data

    data = name_servers2parent(data)
    data = organization2parent('Registrant', 'registrant',  data)
    data = organization2parent('Administrative', 'admin', data)
    data = organization2parent('Technical', 'tech', data)
    data = str2datetime(data)
    data = standardize_status(data)
    return data

def standardize_status(data):
    from stringcase import pascalcase, snakecase
    if 'status' in data:
        if type(data['status']) == str:
            extract_data = data['status']
            del data['status']
            data['status'] = {}

            for d in extract_data.split(','):
                data['status'][snakecase(d.lstrip())] = True

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

            for d in extract_data['name_servers']:
                data['name_servers'].append(d.split(" ")[0])

            data['name_servers'] = list(set(data['name_servers']))
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
                '%d-%b-%Y %H:%M:%S'
            ).replace(tzinfo=pytz.timezone(country_timezones['bn'][0]))

    # 有効期限
    if 'expiration' in data:
        if type(data['expiration']) == str:
            data['expiration'] = datetime.datetime.strptime(
                data['expiration'],
                '%d-%b-%Y %H:%M:%S'
            ).replace(tzinfo=pytz.timezone(country_timezones['bn'][0]))

    # 最終更新
    if 'updated' in data:
        if type(data['updated']) == str:
            data['updated'] = datetime.datetime.strptime(
                data['updated'],
                '%d-%b-%Y %H:%M:%S'
            ).replace(tzinfo=pytz.timezone(country_timezones['bn'][0]))

    return data
</macro>


## Template
## =======================================================

----------------------------------------------------------------------
 BNNIC WHOIS Server
----------------------------------------------------------------------

The following data is provided for information purposes only.

<group del="_ignore_">
Registrar:   {{ registrar_name | ORPHRASE }}

    Domain Name:		{{ domain_name | ORPHRASE | lower }}
    Creation Date:		{{ created | ORPHRASE }}
    Modified Date:		{{ updated | ORPHRASE }}
    Expiration Date:		{{ expiration | ORPHRASE }}
    Domain Status:		{{ status }}


<group name="{{ organization_type }}">
{{ _start_ }}
    {{ organization_type }}:

        Name:           {{ organization | ORPHRASE }}
        Email:          {{ email }}
{{ _end_ }}
</group>

<group name="{{ organization_type }}">
{{ _start_ }}
    {{ organization_type }} Contact:

        Name:           {{ organization | ORPHRASE }}
        Email:          {{ email }}
{{ _end_ }}
</group>

<group name="name_servers" del="_ignore_ns_">
    Name Servers:{{ _start_ }}
        {{ name_servers | ORPHRASE | lower | to_list | joinmatches }}
        {{ name_servers | ORPHRASE | lower | to_list | joinmatches }}  ({{ _ignore_ns_ | to_list | joinmatches }})
{{ _end_ }}
</group>

%%% end %%% {{ _ignore_ }} %%% end %%%
</group>

<output macro="unpack" />
