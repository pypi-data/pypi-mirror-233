## Copyright (c) 2023 Blacknon. All rights reserved.
## Use of this source code is governed by an MIT license
## that can be found in the LICENSE file.
## =======================================================

## NOTE: `outzone`, `delete` はよくわからんのですっとばす

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
    data = organization2parent('registrant', 'registrant', data)
    data = organization2parent('admin', 'admin', data)
    data = organization2parent('tech', 'tech', data)
    data = organization2parent('registrar', 'registrar', data)
    data = dnssec2parent(data)
    data = name_servers2parent(data)

    return data

def organization2parent(organization_type , organization_type_name, data):
    if organization_type in data:
        if type(data[organization_type]) == dict:
            extract_data = data[organization_type]
            del data[organization_type]

            for d in extract_data:
                data["{0}_{1}".format(organization_type_name,d)] = extract_data[d]
    return data

def dnssec2parent(data):
    if 'dnssec' in data:
        dns_keys = [data['dnssec']['dns_keys']]
        data['dns_keys'] = dns_keys

        del data['dnssec']

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

def delete_in_not_disclosed(data):
    updated_data = {}
    for d in data:
        if "Not Disclosed - Visit www.internet.ee for webbased WHOIS" in data[d]:
            continue
        updated_data[d] = data[d]
    data = updated_data
    return data
</macro>



## Template
## =======================================================

Search results may not be used for commercial, advertising, recompilation,
repackaging, redistribution, reuse, obscuring or other similar activities.

Estonia .ee Top Level Domain WHOIS server
<group macro="delete_in_not_disclosed">
Domain:
name:       {{ domain_name }}
status:     {{ status }} ({{ _ignore_ }})
registered: {{ created | ORPHRASE }}
changed:    {{ updated | ORPHRASE }}
expire:     {{ expiration | ORPHRASE }}
outzone:
delete:

<group name="registrant" macro="delete_in_not_disclosed">
Registrant:{{ _start_ }}
name:       {{ name | ORPHRASE }}
org id:     {{ id | ORPHRASE }}
country:    {{ country | ORPHRASE }}
email:      {{ email | ORPHRASE }}
phone:      {{ phone | ORPHRASE }}
changed:    {{ updated | ORPHRASE }}
{{ _end_ }}
</group>

<group name="admin" macro="delete_in_not_disclosed">
Administrative contact:{{ _start_ }}
name:       {{ name | ORPHRASE }}
email:      {{ email | ORPHRASE }}
changed:    {{ updated | ORPHRASE }}
{{ _end_ }}
</group>

<group name="tech" macro="delete_in_not_disclosed">
Technical contact:{{ _start_ }}
name:       {{ name | ORPHRASE }}
email:      {{ email | ORPHRASE }}
changed:    {{ updated | ORPHRASE }}
{{ _end_ }}
</group>

<group name="registrar" macro="delete_in_not_disclosed">
Registrar:{{ _start_ }}
name:       {{ name | ORPHRASE }}
url:        {{ url | ORPHRASE }}
phone:      {{ phone | ORPHRASE }}
changed:    {{ updated | ORPHRASE }}
{{ _end_ }}
</group>

<group name="name_servers" macro="delete_in_not_disclosed">
Name servers:{{ _start_ }}
nserver:   {{ name_servers | ORPHRASE | to_list | joinmatches }}
changed:   {{ updated | ORPHRASE }}
{{ _end_ }}
</group>

<group name="dnssec">
DNSSEC:{{ _start_ }}
dnskey:   {{ dns_keys | ORPHRASE }}
changed:  {{ updated | ORPHRASE }}
{{ _end_ }}
</group>

</group>

Estonia .ee Top Level Domain WHOIS server
More information at http://internet.ee


<output macro="unpack" />
