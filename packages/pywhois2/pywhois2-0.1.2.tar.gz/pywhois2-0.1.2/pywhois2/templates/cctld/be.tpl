## Copyright (c) 2023 Blacknon. All rights reserved.
## Use of this source code is governed by an MIT license
## that can be found in the LICENSE file.
## =======================================================

## NOTE: Registrantはコマンドから取れないため取得しない

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

    data = str2datetime(data)
    data = standardize_status(data)
    data = registrar2parent(data)
    data = tech2parent(data)
    data = dnssec2parent(data)
    data = name_servers2parent(data)

    return data


def standardize_status(data):
    from stringcase import pascalcase, snakecase
    if 'status' in data:
        if type(data['status']['status']) == list:
            extract_data = data['status']['status']
            del data['status']
            data['status'] = {}

            for d in extract_data:
                data['status'][snakecase(d.lstrip())] = True

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
                '%a %b %d %Y'
            ).replace(tzinfo=pytz.timezone(country_timezones['be'][0]))

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

def registrar2parent(data):
    if 'registrar_organization' in data:
        extract_data = data['registrar_organization']
        if type(extract_data) == dict:
            del data['registrar_organization']

            for d in extract_data:
                data[d] = extract_data[d]

    return data

def tech2parent(data):
    if 'tech_organization' in data:
        extract_data = data['tech_organization']
        if type(extract_data) == dict:
            del data['tech_organization']

            for d in extract_data:
                data[d] = extract_data[d]

    return data

def dnssec2parent(data):
    if 'dnssec' in data:
        extract_data = data['dnssec']
        if type(extract_data) == dict:
            del data['dnssec']

            for d in extract_data:
                data[d] = extract_data[d]

    return data
</macro>


## Template
## =======================================================

% .be Whois Server 6.1
%
% The WHOIS service offered by DNS Belgium and the access to the records in the DNS Belgium
% WHOIS database are provided for information purposes only. It allows
% persons to check whether a specific domain name is still available or not
% and to obtain information related to the registration records of
% existing domain names.
%
% DNS Belgium cannot, under any circumstances, be held liable where the stored
% information would prove to be incomplete or inaccurate in any sense.
%
% By submitting a query you agree not to use the information made available
% to:
%   - allow, enable or otherwise support the transmission of unsolicited,
%     commercial advertising or other solicitations whether via email or otherwise;
%   - target advertising in any possible way;
%   - to cause nuisance in any possible way to the domain name holders by sending
%     messages to them (whether by automated, electronic processes capable of
%     enabling high volumes or other possible means).
%
% Without prejudice to the above, it is explicitly forbidden to extract, copy
% and/or use or re-utilise in any form and by any means (electronically or
% not) the whole or a quantitatively or qualitatively substantial part
% of the contents of the WHOIS database without prior and explicit permission
% by DNS Belgium, nor in any attempt thereof, to apply automated, electronic
% processes to DNS Belgium (or its systems).
%
% You agree that any reproduction and/or transmission of data for commercial
% purposes will always be considered as the extraction of a substantial
% part of the content of the WHOIS database.
%
% By submitting the query you agree to abide by this policy and accept that
% DNS Belgium can take measures to limit the use of its whois services in order to
% protect the privacy of its registrants or the integrity of the database.
%

<group>
Domain:	{{ domain_name }}
Status:	NOT AVAILABLE
Registered:	{{ created | ORPHRASE }}

Registrant:
	Not shown, please visit www.dnsbelgium.be for webbased whois.

<group name="tech_organization">
Registrar Technical Contacts:{{ _start_ }}
	Organisation:   {{ tech_organization | ORPHRASE }}
	Language:       {{ tech_language }}
	Phone:  {{ tech_phone }}
{{ _end_ }}
</group>

<group name="registrar_organization">
Registrar:{{ _start_ }}
	Name:	{{ registrar_organization | ORPHRASE }}
	Website:	{{ registrar_url }}
</group>

<group name="name_servers">
Nameservers:{{ _start_ }}
	{{ name_servers | ORPHRASE | to_list | joinmatches }}
{{ _end_ }}
</group>

<group name="dnssec">
Keys:{{ _start_ }}
	{{ dnssec | ORPHRASE }}
{{ _end_ }}
</group>

<group name="status">
Flags:{{ _start_ }}
	{{ status | ORPHRASE | to_list | joinmatches }}
{{ _end_ }}
</group>

Please visit www.dnsbelgium.be for more info.

</group>


<output macro="unpack" />
