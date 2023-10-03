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

    data = registrar_parse(data)
    data = name_servers2parent(data)
    data = str2datetime(data)

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
                '%Y.%m.%d %H:%M:%S'
            ).replace(tzinfo=pytz.timezone(country_timezones['nl'][0]))

    # 有効期限
    if 'expiration' in data:
        if type(data['expiration']) == str:
            data['expiration'] = datetime.datetime.strptime(
                data['expiration'],
                '%Y.%m.%d %H:%M:%S'
            ).replace(tzinfo=pytz.timezone(country_timezones['nl'][0]))

    # 最終更新
    if 'updated' in data:
        if type(data['updated']) == str:
            data['updated'] = datetime.datetime.strptime(
                data['updated'],
                '%Y.%m.%d %H:%M:%S'
            ).replace(tzinfo=pytz.timezone(country_timezones['nl'][0]))

    return data

def registrar_parse(data):
    if 'registrar' in data:
        extract_data = []
        for d in data['registrar']['line']:
            extract_data.append(d.rstrip())
        del data['registrar']

        data['registrar_name'] = extract_data[0]
        data['registrar_address'] = ", ".join(extract_data[1:3])
        data['reststrar_phone'] = extract_data[4].split(" ")[-1]
        data['reststrar_fax'] = extract_data[5].split(" ")[-1]
        data['reststrar_email'] = extract_data[6].split(" ")[-1]
    return data

</macro>


## Template
## =======================================================

<group>
DOMAIN NAME:           {{ domain_name | ORPHRASE }}
registrant type:       {{ registrant_type }}
<group name="name_servers" del="_ignore_">
nameservers:           {{ name_servers | lower | to_list | joinmatches }}. {{ _ignore_ | _line_ | strip('\r') }}
                       {{ name_servers | lower | to_list | joinmatches }}. {{ _ignore_ | _line_ | strip('\r') }}
</group>
created:               {{ created | ORPHRASE }}
last modified:         {{ updated | ORPHRASE }}
renewal date:          {{ expiration | ORPHRASE }}


dnssec:                {{ dnssec | ORPHRASE }}
DS:                    {{ dns_keys | ORPHRASE | to_list | joinmatches }}

<group name="registrar">
REGISTRAR:{{ _start_ }}
{{ line | _line_ | to_list | joinmatches }}
</group>

WHOIS database responses: {{ ignore }}
</group>

WHOIS displays data with a delay not exceeding 15 minutes in relation to the .pl Registry system

<output macro="unpack" />
