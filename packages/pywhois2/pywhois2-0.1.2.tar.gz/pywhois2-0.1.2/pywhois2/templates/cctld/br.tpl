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
    data = registrant_lookup(data)
    data = tech_lookup(data)
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

def registrant_lookup(data):
    if 'registrant_id' in data:
        if data['registrant_id'] in data:
            extract_data = data[data['registrant_id']]

            del data[data['registrant_id']]
            del data['registrant_id']

            for d in extract_data:
                data['registrant_{0}'.format(d)] = extract_data[d]

    return data

def tech_lookup(data):
    if 'tech_id' in data:
        if data['tech_id'] in data:
            extract_data = data[data['tech_id']]

            del data[data['tech_id']]
            del data['tech_id']

            for d in extract_data:
                data['tech_{0}'.format(d)] = extract_data[d]

    return data

def str2datetime(data):
    import datetime
    import pytz
    from pytz import country_timezones

    format = '%Y%m%d'
    if 'created' in data:
        data['created'] = datetime.datetime.strptime(
            data['created'],
            format
        ).replace(tzinfo=pytz.timezone(country_timezones['br'][0]))

    if 'updated' in data:
        data['updated'] = datetime.datetime.strptime(
            data['updated'],
            format
        ).replace(tzinfo=pytz.timezone(country_timezones['br'][0]))

    if 'expiration' in data:
        data['expiration'] = datetime.datetime.strptime(
            data['expiration'],
            format
        ).replace(tzinfo=pytz.timezone(country_timezones['br'][0]))

    return data

</macro>

## Template
## =======================================================

% Copyright (c) Nic.br
%  The use of the data below is only permitted as described in
%  full by the Use and Privacy Policy at https://registro.br/upp ,
%  being prohibited its distribution, commercialization or
%  reproduction, in particular, to use it for advertising or
%  any similar purpose.
%  2023-09-15T03:43:08-03:00 - IP: 150.246.74.245

<group macro="str2datetime" del="_ignore_">
domain:      {{ domain_name }}
owner:       {{ registrant_organization | ORPHRASE }}
owner-c:     {{ registrant_id }}
tech-c:      {{ tech_id }}
nserver:     {{ name_servers | lower | ORPHRASE | to_list | joinmatches }}
created:     {{ created }}
created:     {{ created }} #{{ _ignore_ }}
changed:     {{ updated }}
changed:     {{ updated }} #{{ _ignore_ }}
expires:     {{ expiration }}
expires:     {{ expiration }} #{{ _ignore_ }}
status:      {{ status }}

<group name="{{ nic_hdl_br }}" macro="str2datetime" del="_ignore_">
nic-hdl-br:  {{ nic_hdl_br }}
person:      {{ name | ORPHRASE }}
created:     {{ created }}
created:     {{ created }} #{{ _ignore_ }}
changed:     {{ updated }}
changed:     {{ updated }} #{{ _ignore_ }}
</group>

</group>

% Security and mail abuse issues should also be addressed to
% cert.br, http://www.cert.br/ , respectivelly to cert@cert.br
% and mail-abuse@cert.br
%
% whois.registro.br accepts only direct match queries. Types
% of queries are: domain (.br), registrant (tax ID), ticket,
% provider, CIDR block, IP and ASN.

<output macro="unpack" />
