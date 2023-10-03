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

    data = organization2parent('tech', 'admin', data)
    data = organization2parent('holder', 'registrant', data)
    data = organization2parent('registrar', 'registrar', data)
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
        extract_data = data['status']
        if type(extract_data) == str:
            del data['status']
            data['status'] = {}
            for line in extract_data.split(","):
                data['status'][line] = True
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

<group>
[Domain]
Domain: {{ domain_name }}
Status: {{ status }}

<group name="{{ group_type }}">
{{ _start_ }}
[{{ group_type | lower }}]
    Type: {{ type | ORPHRASE }}
    Name: {{ name | ORPHRASE }}
    Address: {{ address | ORPHRASE }}
    RegNr: {{ id | ORPHRASE }}
Visit: https://www.nic.lv/whois/contact/google.lv to contact.
{{ _end_ }}
</group>

<group name="{{ group_type }}">
{{ _start_ }}
[{{ group_type | lower }}]
Type: {{ type | ORPHRASE }}
Visit: https://www.nic.lv/whois/contact/google.lv to contact.
{{ _end_ }}
</group>

[Nservers]
Nserver: {{ name_servers | ORPHRASE | to_list | joinmatches }}

[Whois]
Updated: {{ updated }}
</group>

[Disclaimer]
% The WHOIS service is provided solely for informational purposes.
%
% It is permitted to use the WHOIS service only for technical or administrative
% needs associated with the operation of the Internet or in order to contact
% the domain name holder over legal problems.
%
% Requestor will not use information obtained using WHOIS:
% * To allow, enable or in any other way to support sending of unsolicited mails (spam)
% * for any kind of advertising
% * to disrupt Internet stability and security
%
% It is not permitted to obtain (including copying) or re-use in any form or
% by any means all or quantitatively or qualitatively significant part
% of the WHOIS without NIC's express permission.

<output macro="unpack" />
