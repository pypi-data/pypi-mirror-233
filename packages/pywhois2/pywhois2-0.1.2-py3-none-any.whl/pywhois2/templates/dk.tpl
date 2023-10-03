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

    return data

def status2parent(data):
    from stringcase import pascalcase, snakecase
    if 'status' in data:
        extract_data = data['status']
        if type(extract_data) == str:
            del data['status']

            data['status'] = {}
            for d in extract_data.split(","):
                key = snakecase(d.lstrip().lower())
                if key == "active":
                    key = 'ok'
                data['status'][key] = True

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
                '%Y-%m-%d'
            ).replace(tzinfo=pytz.timezone(country_timezones['dk'][0]))

    # 有効期限
    if 'expiration' in data:
        if type(data['expiration']) == str:
            data['expiration'] = datetime.datetime.strptime(
                data['expiration'],
                '%Y-%m-%d'
            ).replace(tzinfo=pytz.timezone(country_timezones['dk'][0]))

    # 最終更新
    if 'updated' in data:
        if type(data['updated']) == str:
            data['updated'] = datetime.datetime.strptime(
                data['updated'],
                '%Y-%m-%d'
            ).replace(tzinfo=pytz.timezone(country_timezones['dk'][0]))

    return data
</macro>


## Template
## =======================================================

# Copyright (c) 2002 - 2023 by DK Hostmaster A/S
#
# Version: 5.1.0
#
# The data in the DK Whois database is provided by DK Hostmaster A/S
# for information purposes only, and to assist persons in obtaining
# information about or related to a domain name registration record.
# We do not guarantee its accuracy. We will reserve the right to remove
# access for entities abusing the data, without notice.
#
# Any use of this material to target advertising or similar activities
# are explicitly forbidden and will be prosecuted. DK Hostmaster A/S
# requests to be notified of any such activities or suspicions thereof.

<group macro="str2datetime, status2parent">
Domain:               {{ domain_name | ORPHRASE }}
Registered:           {{ created }}
Expires:              {{ expiration }}
Registrar:            {{ registrar_name}}
VID:                  {{ vid }}
DNSSEC:               {{ dnssec | ORPHRASE }}
Status:               {{ status }}

<group name="name_servers">
Nameservers{{ _start_ }}
Hostname:             {{ name_servers | ORPHRASE | to_list | joinmatches }}
{{ _end_ }}
</group>
</group>


<output macro="unpack" />
