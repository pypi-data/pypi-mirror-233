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

    data = organization2parent('registrant', 'registrant', data)
    data = organization2parent('admin', 'admin', data)
    data = organization2parent('tech', 'tech', data)
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

</macro>


## Template
## =======================================================

% SaudiNIC Whois server.
% Rights restricted by copyright.
% http://nic.sa/en/view/whois-cmd-copyright

<group>
Domain Name: {{ domain_name }}

<group name="registrant">
Registrant:{{ _start_ }}
{{ organization | ORPHRASE }}
Address: ************************* *********
***** *************
Unknown
{{ _end_ }}
</group>

<group name="admin">
Administrative Contact:{{ _start_ }}
Dnet *****
Address: ***** *****
***** *****
*****
{{ _end_ }}
</group>

<group name="tech">
Technical Contact:{{ _start_ }}
Domain *****
Address: ***** *****
***** *****
*****
{{ _end_ }}
</group>

<group name="name_servers">
Name Servers:{{ _start_ }}
{{ name_servers | lower | to_list | joinmatches }}
{{ _end_ }}
</group>

DNSSEC: {{ dnssec }}

</group>

<output macro="unpack" />
