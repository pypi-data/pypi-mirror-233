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
            update_d = {}
            for dd in data[d]:
                if type(dd) == dict:
                    update_d.update(dd)
                    update_data[d] = update_d
                else:
                    if d not in update_data:
                        update_data[d] = list()
                    update_data[d].append(dd)
        else:
            update_data[d] = data[d]
    data = update_data

    if 'registrant' in data:
        extract_data = data['registrant']
        del data['registrant']

        data['registrant_name'] = extract_data['line'][0]

    data = name_servers2parent(data)
    data = organization2parent('registrar', 'registrar', data)
    data = str2datetime(data)

    return data

def name_servers2parent(data):
    if 'name_servers' in data:
        extract_data = data['name_servers']['name_servers']
        if type(extract_data) == list:
            del data['name_servers']
            data['name_servers'] = extract_data

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
                data['created'].replace(" GMT+1", " +01:00"),
                '%Y-%b-%d'
            ).replace(tzinfo=pytz.timezone(country_timezones['tr'][0]))

    # 有効期限
    if 'expiration' in data:
        if type(data['expiration']) == str:
            data['expiration'] = datetime.datetime.strptime(
                data['expiration'].replace(" GMT+1", " +01:00"),
                '%Y-%b-%d'
            ).replace(tzinfo=pytz.timezone(country_timezones['tr'][0]))

    # 最終更新
    if 'updated' in data:
        if type(data['updated']) == str:
            data['updated'] = datetime.datetime.strptime(
                data['updated'].replace(" GMT+1", " +01:00"),
                '%Y-%b-%d'
            ).replace(tzinfo=pytz.timezone(country_timezones['tr'][0]))

    return data
</macro>


## Template
## =======================================================

<group>
** Domain Name: {{ domain_name }}
Frozen Status: -
Transfer Status: The domain is LOCKED to transfer.

<group name="registrant">
** Registrant:{{ _start_ }}
   {{ line | _line_ | to_list | joinmatches }}
{{ _end_ }}
</group>

<group name="registrar">
** Registrar:
NIC Handle		: {{ id }}
Organization Name	: {{ organization | ORPHRASE }}
<group>
Address			: {{ address | ORPHRASE | joinmatches(", ") }}
			  {{ address | ORPHRASE | joinmatches(", ") }}
</group>
Phone			: {{ phone | ORPHRASE }}
Fax			: {{ fax | ORPHRASE }}
</group>

<group name="name_servers">
** Domain Servers:{{ _start_ }}
{{ name_servers | lower | to_list | joinmatches }}
{{ name_servers | lower | to_list | joinmatches }} {{ ignore | ORPHRASE }}
{{ _end_ }}
</group>

** Additional Info:
Created on..............: {{ created | ORPHRASE }}.
Expires on..............: {{ expiration | ORPHRASE }}.


** Whois Server:
Last Update Time: {{ ignore }}
</group>

<output macro="unpack" />
