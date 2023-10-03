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

    data = lookup(data)

    return data

def lookup(data):
    registrant_id = ''
    admin_id = ''
    tech_id = ''

    if 'registrar' in data:
        extract_data = data['registrar']
        del data['registrar']

        for d in extract_data:
            data['registrar_{0}'.format(d)] = extract_data[d]

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

    if registrant_id != '':
        if registrant_id in data:
            del data[registrant_id]

    if admin_id != '':
        if admin_id in data:
            del data[admin_id]

    if tech_id != '':
        if tech_id in data:
            del data[tech_id]

    return data

def str2datetime(data):
    import datetime
    if 'created' in data:
        if type(data['created']) == str:
            data['created'] = datetime.datetime.fromisoformat(data['created'])

    if 'updated' in data:
        if type(data['updated']) == str:
            data['updated'] = datetime.datetime.fromisoformat(data['updated'])

    if 'expiration' in data:
        if type(data['expiration']) == str:
            data['expiration'] = datetime.datetime.fromisoformat(data['expiration'])

    return data
</macro>



## Template
## =======================================================

%%
%% This is the AFNIC Whois server.
%%
%% complete date format: YYYY-MM-DDThh:mm:ssZ
%%
%% Rights restricted by copyright.
%% See https://www.afnic.fr/en/domain-names-and-support/everything-there-is-to-know-about-domain-names/find-a-domain-name-or-a-holder-using-whois/
%%
%%

<group macro="str2datetime">
domain:                        {{ domain_name | lower | ORPHRASE }}
status:                        {{ domain_status | lower | ORPHRASE }}
eppstatus:                     {{ domain_epp_status | lower | ORPHRASE }}
hold:                          {{ domain_hold_status | lower | ORPHRASE }}
holder-c:                      {{ registrant_id }}
admin-c:                       {{ admin_id }}
tech-c:                        {{ tech_id }}
Expiry Date:                   {{ expiration }}
created:                       {{ created }}
last-update:                   {{ updated }}
source:                        FRNIC

nserver:                       {{ name_servers | ORPHRASE | to_list | joinmatches }}
source:                        FRNIC

<group name="registrar">
{{ _start_ }}
registrar:                     {{ name | ORPHRASE }}
address:                       {{ address | ORPHRASE | joinmatches(", ") }}
phone:                         {{ phone }}
fax-no:                        {{ fax }}
e-mail:                        {{ email }}
website:                       {{ url }}
anonymous:                     {{ is_anonymous }}
source:                        FRNIC
{{ _end_ }}
</group>

<group name="{{ nic-hdl }}">
nic-hdl:                       {{ nic-hdl }}
type:                          {{ type }}
contact:                       {{ name }}
address:                       {{ address | ORPHRASE | joinmatches(", ") }}
country:                       {{ country }}
phone:                         {{ phone }}
fax-no:                        {{ fax }}
e-mail:                        {{ email }}
registrar:                     {{ registrar }}
anonymous:                     {{ is_anonymous }}
obsoleted:                     {{ is_obsoleted }}
source:                        FRNIC
</group>

</group>

<output macro="unpack" />
