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

    data = lookup(data)

    return data

def lookup(data):
    registrant_id = ''
    admin_id = ''
    tech_id = ''
    zone_id = ''
    billing_id = ''

    if 'registrant_id' in data:
        registrant_id = data['registrant_id']
        if registrant_id in data:
            extract_data = data[registrant_id]
            del data['registrant_id']

            for d in extract_data:
                data['registrant_{0}'.format(d)] = extract_data[d]

    if 'admin_id' in data:
        admin_id = data['admin_id']
        if admin_id in data:
            extract_data = data[data['admin_id']]
            del data['admin_id']

            for d in extract_data:
                data['admin_{0}'.format(d)] = extract_data[d]

    if 'tech_id' in data:
        tech_id = data['tech_id']
        if tech_id in data:
            extract_data = data[tech_id]
            del data['tech_id']

            for d in extract_data:
                data['tech_{0}'.format(d)] = extract_data[d]

    if 'zone_id' in data:
        zone_id = data['zone_id']
        if zone_id in data:
            extract_data = data[zone_id]
            del data['zone_id']

            for d in extract_data:
                data['zone_{0}'.format(d)] = extract_data[d]

    if 'billing_id' in data:
        billing_id = data['billing_id']
        if billing_id in data:
            extract_data = data[billing_id]
            del data['billing_id']

            for d in extract_data:
                data['billing_{0}'.format(d)] = extract_data[d]

    if registrant_id != '':
        if registrant_id in data:
            del data[registrant_id]

    if admin_id != '':
        if admin_id in data:
            del data[admin_id]

    if tech_id != '':
        if tech_id in data:
            del data[tech_id]

    if zone_id != '':
        if zone_id in data:
            del data[zone_id]

    if billing_id != '':
        if billing_id in data:
            del data[billing_id]

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
                '%B %d %Y'
            ).replace(tzinfo=pytz.timezone(country_timezones['is'][0]))

    # 有効期限
    if 'expiration' in data:
        if type(data['expiration']) == str:
            data['expiration'] = datetime.datetime.strptime(
                data['expiration'],
                '%B %d %Y'
            ).replace(tzinfo=pytz.timezone(country_timezones['is'][0]))

    # 最終更新
    if 'updated' in data:
        if type(data['updated']) == str:
            data['updated'] = datetime.datetime.strptime(
                data['updated'],
                '%B %d %Y'
            ).replace(tzinfo=pytz.timezone(country_timezones['is'][0]))

    return data
</macro>


## Template
## =======================================================

% This is the ISNIC Whois server.
%
% Rights restricted by copyright.
% See https://www.isnic.is/en/about/copyright

<group macro="str2datetime">
domain:       {{ domain_name }}
registrant:   {{ registrant_id }}
admin-c:      {{ admin_id }}
tech-c:       {{ tech_id }}
zone-c:       {{ zone_id }}
billing-c:    {{ billing_id }}
nserver:      {{ name_servers | ORPHRASE | to_list | joinmatches }}
dnssec:       {{ dnssec | ORPHRASE }}
created:      {{ created | ORPHRASE }}
expires:      {{ expiration | ORPHRASE }}
source:       ISNIC

<group name="{{ nic_hdl }}" macro="str2datetime">
{{ _start_ }}
role:         {{ organization | ORPHRASE }}
nic-hdl:      {{ nic_hdl }}
address:      {{ address | ORPHRASE | joinmatches(', ') }}
phone:        {{ phone | ORPHRASE }}
e-mail:       {{ email }}
created:      {{ created | ORPHRASE }}
created:      {{ created | _line_ }}
source:       ISNIC{{ _end_ }}
</group>

<group name="{{ nic_hdl }}" macro="str2datetime">
{{ _start_ }}
nic-hdl:      {{ nic_hdl }}
address:      {{ address | ORPHRASE | joinmatches(', ') }}
phone:        {{ phone | ORPHRASE }}
e-mail:       {{ email }}
created:      {{ created | _line_ }}
source:       ISNIC{{ _end_ }}
</group>

</group>


<output macro="unpack" />
