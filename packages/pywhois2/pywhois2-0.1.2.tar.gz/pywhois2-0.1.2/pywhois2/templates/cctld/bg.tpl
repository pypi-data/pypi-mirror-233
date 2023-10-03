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

    data = standardize_status(data)
    data = dnssec2parent(data)
    data = name_servers2parent(data)

    return data


def standardize_status(data):
    from stringcase import pascalcase, snakecase
    if 'status' in data:
        if type(data['status']) == str:
            extract_data = data['status']
            del data['status']
            data['status'] = {}

            for d in extract_data.split(','):
                data['status'][snakecase(d.lstrip())] = True

    return data

def dnssec2parent(data):
    if 'dnssec' in data:
        extract_data = data['dnssec']
        if type(extract_data) == dict:
            del data['dnssec']

            for d in extract_data:
                data[d] = extract_data[d]

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
</macro>


## Template
## =======================================================

<group del="_ignore_">
DOMAIN NAME: {{ domain_name }} ({{ _ignore_ }})
registration status: {{ status | ORPHRASE }}

<group name="name_servers">
NAME SERVER INFORMATION:{{ _start_ }}
{{ name_servers | lower | ORPHRASE | to_list | joinmatches }}
{{ _end_ }}
</group>

<group name="dnssec">
DNSSEC: {{ dnssec }}
</group>

According to REGULATION (EU) 2016/679 OF THE EUROPEAN PARLIAMENT AND
OF THE COUNCIL (GDPR) personal data is not published.
</group>

If you would like to contact the persons responsible for the domain
name, please, use the online WHOIS contact form from the "Info / Whois" menu
at www.register.bg.

<output macro="unpack" />
