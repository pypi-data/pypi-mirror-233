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

    if 'organization' in data:
        data['registrant_organization'] = data['organization']
        del data['organization']

    if 'address' in data:
        data['registrant_address'] = data['address']
        del data['address']

    if 'changed_lines' in data:
        data['created'] = data['changed_lines'][0].split(' ')[-2]
        data['updated'] = data['changed_lines'][-1].split(' ')[-2]

        del data['changed_lines']

    data = lookup(data)
    data = str2datetime(data)

    return data

def lookup(data):
    admin_id = ''
    tech_id = ''
    zone_id = ''

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

    if admin_id != '':
        if admin_id in data:
            del data[admin_id]

    if tech_id != '':
        if tech_id in data:
            del data[tech_id]

    if zone_id != '':
        if zone_id in data:
            del data[zone_id]

    return data

def info_sep(data):
    if 'info' in data:
        data['organization'] = data['info'][0]
        data['address'] = ", ".join(data['info'][1:])

        del data['info']

    return data

def str2datetime(data):
    import datetime
    import pytz
    from pytz import country_timezones

    # 登録年月日
    if 'created' in data:
        if type(data['created']) == str:
            if len(data['created']) == 8:
                data['created'] = datetime.datetime.strptime(
                    data['created'],
                    '%Y%m%d'
                ).replace(tzinfo=pytz.timezone(country_timezones['hk'][0]))
            else:
                del data['created']

    # 有効期限
    if 'expiration' in data:
        if type(data['expiration']) == str:
            if len(data['expiration']) == 10:
                data['expiration'] = datetime.datetime.strptime(
                    data['expiration'],
                    '%d-%m-%Y'
                ).replace(tzinfo=pytz.timezone(country_timezones['hk'][0]))
            else:
                del data['expiration']

    # 最終更新
    if 'updated' in data:
        if type(data['updated']) == str:
            if len(data['updated']) == 8:
                data['updated'] = datetime.datetime.strptime(
                    data['updated'],
                    '%Y%m%d'
                ).replace(tzinfo=pytz.timezone(country_timezones['hk'][0]))
            else:
                del data['updated']

    return data

</macro>


## Template
## =======================================================

% The data in the WHOIS database of the .il registry is provided
% by ISOC-IL for information purposes, and to assist persons in
% obtaining information about or related to a domain name
% registration record. ISOC-IL does not guarantee its accuracy.
% By submitting a WHOIS query, you agree that you will use this
% Data only for lawful purposes and that, under no circumstances
% will you use this Data to: (1) allow, enable, or otherwise
% support the transmission of mass unsolicited, commercial
% advertising or solicitations via e-mail (spam);
% or  (2) enable high volume, automated, electronic processes that
% apply to ISOC-IL (or its systems).
% ISOC-IL reserves the right to modify these terms at any time.
% By submitting this query, you agree to abide by this policy.

<group macro="info_sep">
query:        {{ ignore }}

reg-name:     {{ ignore }}
domain:       {{ domain_name }}

descr:        {{ info | ORPHRASE | to_list | joinmatches }}
phone:        {{ registrar_phone | ORPHRASE }}
fax-no:       {{ registrar_fax | ORPHRASE }}
e-mail:       {{ registrar_email | ORPHRASE }}
admin-c:      {{ admin_id }}
tech-c:       {{ tech_id }}
zone-c:       {{ zone_id }}
nserver:      {{ name_servers | lower | ORPHRASE | to_list | joinmatches }}
validity:     {{ expiration | ORPHRASE }}
DNSSEC:       {{ dnssec }}
status:       {{ status | ORPHRASE }}
changed:      {{ changed_lines | _line_ | to_list | joinmatches }}

<group name="{{ nic_hdl }}" macro="info_sep, str2datetime">
person:       {{ name | ORPHRASE }}
address      {{ info | ORPHRASE | to_list | joinmatches }}
phone:        {{ phone | ORPHRASE }}
fax-no:       {{ fax | ORPHRASE }}
e-mail:       {{ email | ORPHRASE }}
nic-hdl:      {{ nic_hdl }}
changed:      Managing Registrar {{ updated | ORPHRASE }}
</group>
</group>

registrar name: Domain The Net Technologies Ltd
registrar info: https://www.domainthenet.com

% Rights to the data above are restricted by copyright.

<output macro="unpack" />
