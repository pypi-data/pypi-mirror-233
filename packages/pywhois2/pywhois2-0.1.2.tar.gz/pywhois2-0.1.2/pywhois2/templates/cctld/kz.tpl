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

    data = organization2parent('admin', 'admin', data)
    data = organization2parent('registrant', 'registrant', data)
    data = status2parent(data)
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

def status2parent(data):
    from stringcase import pascalcase, snakecase
    if 'status' in data:
        extract_data = data['status']['status']
        if type(extract_data) == list:
            del data['status']
            data['status'] = {}
            for line in extract_data:
                data['status'][snakecase(line.split(" ")[0])] = True
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
                '%Y-%m-%d %H:%M:%S (GMT%z)'
            ).replace(tzinfo=pytz.timezone(country_timezones['kz'][0]))

    # 有効期限
    if 'expiration' in data:
        if type(data['expiration']) == str:
            data['expiration'] = datetime.datetime.strptime(
                data['expiration'].replace('+0:00', '+00:00'),
                '%Y-%m-%d %H:%M:%S (GMT%z)'
            ).replace(tzinfo=pytz.timezone(country_timezones['kz'][0]))

    # 最終更新
    if 'updated' in data:
        if type(data['updated']) == str:
            data['updated'] = datetime.datetime.strptime(
                data['updated'].replace('+0:00', '+00:00'),
                '%Y-%m-%d %H:%M:%S (GMT%z)'
            ).replace(tzinfo=pytz.timezone(country_timezones['kz'][0]))

    return data
</macro>


## Template
## =======================================================

Whois Server for the KZ top level domain name.
This server is maintained by KazNIC Organization, a ccTLD manager for Kazakhstan Republic.

<group>
Domain Name............: {{ domain_name }}

<group name="registrant">
Organization Using Domain Name{{ _start_ }}
Name...................: {{ name | ORPHRASE }}
Organization Name......: {{ organization | ORPHRASE }}
Street Address.........: {{ address | ORPHRASE | joinmatches(", ") }}
City...................: {{ address | ORPHRASE | joinmatches(", ") }}
State..................: {{ address | ORPHRASE | joinmatches(", ") }}
Postal Code............: {{ zip_code | ORPHRASE }}
Country................: {{ country }}
{{ _end_ }}
</group>

<group name="admin">
Administrative Contact/Agent{{ _start_ }}
NIC Handle.............: {{ nic_id }}
Name...................: {{ name }}
Phone Number...........: {{ phone }}
Fax Number.............: {{ fax }}
Email Address..........: {{ email }}
{{ _end_ }}
</group>

Nameserver in listed order

Primary server.........: {{ name_servers | ORPHRASE | to_list | joinmatches }}
Primary ip address.....: {{ ignore }}

Secondary server.......: {{ name_servers | ORPHRASE | to_list | joinmatches }}
Secondary ip address...: {{ ignore }}

Domain created: {{ created | ORPHRASE }}
Last modified : {{ updated | ORPHRASE }}
<group name="status">
Domain status : {{ status | ORPHRASE | to_list | joinmatches }}
                {{ status | ORPHRASE | to_list | joinmatches }}
</group>

Registar created: HOSTER.KZ
Current Registar: HOSTER.KZ
</group>

<output macro="unpack" />
