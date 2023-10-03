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
                up_d = {}
                for dd in data[d]:
                    for ddd in dd:
                        up_d[ddd] = dd[ddd]
                data[d] = up_d

        elif type(data[d]) == dict:
            if not data[d]:
                continue
        update_data[d] = data[d]
    data = update_data

    data = organization2parent('registrant', 'registrant', data)
    data = organization2parent('admin', 'admin', data)
    data = organization2parent('technical', 'tech', data)
    data = organization2parent('registrar', 'registrar', data)
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

def name_servers2parent(data):
    if 'name_servers' in data:
        extract_data = data['name_servers']['name_servers']
        if type(extract_data) == list:
            del data['name_servers']
            data['name_servers'] = extract_data

    return data

def standardize_status(data):
    from stringcase import pascalcase, snakecase
    if 'status' in data:
        if type(data['status']) == str:
            extract_data = data['status']
            del data['status']
            data['status'] = {}

            for d in extract_data.split(","):
                data['status'][snakecase(d.lstrip())] = True

    return data

</macro>

## Template
## =======================================================

*********************************************************************
* Please note that the following result could be a subgroup of      *
* the data contained in the database.                               *
*                                                                   *
* Additional information can be visualized at:                      *
* http://web-whois.nic.it                                           *
*********************************************************************

<group macro="standardize_status">
Domain:             {{ domain_name }}
Status:             {{ status }}
Signed:             no
Created:            {{ created | ORPHRASE }}
Last Update:        {{ updated | ORPHRASE }}
Expire Date:        {{ expiration | ORPHRASE }}

<group name="{{ group_type }}">
{{ group_type | lower }}
  Name:             {{ name | ORPHRASE }}
  Organization:     {{ organization | ORPHRASE }}
<group>
  Address:          {{ address | ORPHRASE | joinmatches(", ") }}
                    {{ address | ORPHRASE | joinmatches(", ") }}
</group>
  Created:          {{ created | ORPHRASE }}
  Last Update:      {{ updated | ORPHRASE }}
</group>

<group name="{{ group_type }}">
{{ group_type | lower }} Contact
  Name:             {{ name | ORPHRASE }}
  Organization:     {{ organization | ORPHRASE }}
<group>
  Address:          {{ address | ORPHRASE | joinmatches(", ") }}
                    {{ address | ORPHRASE | joinmatches(", ") }}
</group>
  Created:          {{ created | ORPHRASE }}
  Last Update:      {{ updated | ORPHRASE }}
</group>

<group name="{{ group_type }}">
{{ group_type | lower }} Contacts
  Name:             {{ name | ORPHRASE }}
  Organization:     {{ organization | ORPHRASE }}
<group>
  Address:          {{ address | ORPHRASE | joinmatches(", ") }}
                    {{ address | ORPHRASE | joinmatches(", ") }}
</group>
  Created:          {{ created | ORPHRASE }}
  Last Update:      {{ updated | ORPHRASE }}
</group>


<group name="{{ group_type }}">
{{ group_type | lower }}
  Name:             {{ name | ORPHRASE }}
  Organization:     {{ organization | ORPHRASE }}
  Web:              {{ url }}
  DNSSEC:           {{ dnssec }}
</group>

<group name="name_servers">
Nameservers{{ _start_ }}
  {{ name_servers | ORPHRASE | to_list | joinmatches }}
{{ _end_ }}
</group>

%%% end %%% {{ ignore }} %%% end %%%
</group>


<output macro="unpack" />
