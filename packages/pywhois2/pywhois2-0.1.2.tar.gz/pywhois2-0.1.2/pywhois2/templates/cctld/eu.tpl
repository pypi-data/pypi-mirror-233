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
    data = organization2parent('on_site', 'on_site', data)
    data = organization2parent('tech', 'tech', data)
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

% The WHOIS service offered by EURid and the access to the records
% in the EURid WHOIS database are provided for information purposes
% only. It allows persons to check whether a specific domain name
% is still available or not and to obtain information related to
% the registration records of existing domain names.
%
% EURid cannot, under any circumstances, be held liable in case the
% stored information would prove to be wrong, incomplete or not
% accurate in any sense.
%
% By submitting a query you agree not to use the information made
% available to:
%
% - allow, enable or otherwise support the transmission of unsolicited,
%   commercial advertising or other solicitations whether via email or
%   otherwise;
% - target advertising in any possible way;
%
% - to cause nuisance in any possible way to the registrants by sending
%   (whether by automated, electronic processes capable of enabling
%   high volumes or other possible means) messages to them.
%
% Without prejudice to the above, it is explicitly forbidden to extract,
% copy and/or use or re-utilise in any form and by any means
% (electronically or not) the whole or a quantitatively or qualitatively
% substantial part of the contents of the WHOIS database without prior
% and explicit permission by EURid, nor in any attempt hereof, to apply
% automated, electronic processes to EURid (or its systems).
%
% You agree that any reproduction and/or transmission of data for
% commercial purposes will always be considered as the extraction of a
% substantial part of the content of the WHOIS database.
%
% By submitting the query you agree to abide by this policy and accept
% that EURid can take measures to limit the use of its WHOIS services
% in order to protect the privacy of its registrants or the integrity
% of the database.
%
% The EURid WHOIS service on port 43 (textual whois) never
% discloses any information concerning the registrant.
% Registrant and on-site contact information can be obtained through use of the
% webbased WHOIS service available from the EURid website www.eurid.eu
%
% WHOIS google.eu

<group>
Domain: {{ domain_name }}
Script: LATIN

<group name="registrant">
Registrant:{{ _start_ }}
        Organisation: {{ organization | ORPHRASE }}
        Language: {{ lang }}
        Email: {{ email }}
{{ _end_ }}
</group>

<group name="on_site">
On-site(s):{{ _start_ }}
        Organisation: {{ organization | ORPHRASE }}
        Language: {{ lang }}
        Email: {{ email }}
{{ _end_ }}
</group>

<group name="tech">
Technical:{{ _start_ }}
        Organisation: {{ organization | ORPHRASE }}
        Language: {{ lang }}
        Email: {{ email }}
{{ _end_ }}
</group>

<group name="registrar">
Registrar:{{ _start_ }}
        Name: {{ name | ORPHRASE }}
        Website: {{ url }}
{{ _end_ }}
</group>

<group name="name_servers">
Name servers:{{ _start_ }}
        {{ name_servers | strip(' ') | ORPHRASE | to_list | joinmatches }}
{{ _end_ }}
</group>

Please visit www.eurid.eu for more info.
</group>


<output macro="unpack" />
