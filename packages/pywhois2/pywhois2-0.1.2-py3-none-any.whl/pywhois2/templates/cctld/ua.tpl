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

    data = standardize_status(data)
    data = organization2parent('registrar', 'registrar', data)
    data = organization2parent('registrant', 'registrant', data)
    data = organization2parent('admin', 'admin', data)
    data = str2datetime(data)

    return data

def standardize_status(data):
    from stringcase import pascalcase, snakecase
    if 'status' in data:
        if type(data['status']) == list:
            extract_data = data['status']
            del data['status']
            data['status'] = {}

            for d in extract_data:
                data['status'][snakecase(d.lstrip())] = True

    return data

def organization2parent(organization_type , organization_type_name, data):
    if organization_type in data:
        if type(data[organization_type]) == dict:
            extract_data = data[organization_type]
            del data[organization_type]

            for d in extract_data:
                data["{0}_{1}".format(organization_type_name,d)] = extract_data[d]
    return data

def str2datetime(data):
    import datetime
    import pytz
    from pytz import country_timezones

    # 登録年月日
    if 'created' in data:
        if type(data['created']) == str:
            data['created'] = datetime.datetime.strptime(
                "{0}{1}".format(data['created'], ":00"),
                '%Y-%m-%d %H:%M:%S%z'
            ).replace(tzinfo=pytz.timezone(country_timezones['ua'][0]))

    # 有効期限
    if 'expiration' in data:
        if type(data['expiration']) == str:
            data['expiration'] = datetime.datetime.strptime(
                "{0}{1}".format(data['expiration'], ":00"),
                '%Y-%m-%d %H:%M:%S%z'
            ).replace(tzinfo=pytz.timezone(country_timezones['ua'][0]))

    # 最終更新
    if 'updated' in data:
        if type(data['updated']) == str:
            data['updated'] = datetime.datetime.strptime(
                "{0}{1}".format(data['updated'], ":00"),
                '%Y-%m-%d %H:%M:%S%z'
            ).replace(tzinfo=pytz.timezone(country_timezones['ua'][0]))

    return data

</macro>


## Template
## =======================================================

% This is the Ukrainian Whois query server #C.
% The Whois is subject to Terms of use
% See https://hostmaster.ua/services/
%
% IN THE PROCESS OF DELEGATION OF A DOMAIN NAME,
% THE REGISTRANT IS AN ENTITY WHO USES AND MANAGES A CERTAIN DOMAIN NAME,
% AND THE REGISTRAR IS A BUSINESS ENTITY THAT PROVIDES THE REGISTRANT
% WITH THE SERVICES NECESSARY FOR THE TECHNICAL MAINTENANCE OF THE REGISTRATION AND OPERATION OF THE DOMAIN NAME.
% FOR INFORMATION ABOUT THE REGISTRANT OF THE DOMAIN NAME, YOU SHOULD CONTACT THE REGISTRAR.

<group>
domain:           {{ domain_name }}
license:          {{ domain_license }}
nserver:          {{ name_servers | strip(' ') | ORPHRASE | to_list | joinmatches }}
status:           {{ status | to_list | joinmatches }}
created:          {{ created | ORPHRASE }}
modified:         {{ updated | ORPHRASE }}
expires:          {{ expiration | ORPHRASE }}
source:           UAEPP

<group name="registrar" macro="str2datetime">
% Registrar:{{ _start_ }}
% ==========
registrar:        {{ id }}
organization:     {{ organization | ORPHRASE }}
organization-loc: {{ organization_local | ORPHRASE }}
url:              {{ url }}
city:             {{ address | ORPHRASE | joinmatches(", ") }}
country:          {{ country | ORPHRASE }}
abuse-email:      {{ email | ORPHRASE }}
abuse-postal:     {{ address | ORPHRASE | joinmatches(", ") }}
source:           UAEPP
</group>

<group name="registrant" macro="str2datetime">
% Registrant:{{ _start_ }}
% ===========
person:           {{ name | ORPHRASE }}
person-loc:       {{ name_local | ORPHRASE }}
organization-loc: {{ organization_local | ORPHRASE }}
e-mail:           {{ email | ORPHRASE }}
address:          {{ address | ORPHRASE | joinmatches(", ") }}
address-loc:      {{ address | ORPHRASE | joinmatches(", ") }}
address-loc:      {{ address | ORPHRASE | joinmatches(", ") }}
address-loc:      {{ address | ORPHRASE | joinmatches(", ") }}
postal-code-loc:  {{ zip_code | ORPHRASE }}
country-loc:      {{ country | ORPHRASE }}
phone:            {{ phone }}
fax:              {{ fax }}
status:           {{ status | to_list | joinmatches }}
created:          {{ created | ORPHRASE }}
source:           UAEPP
</group>

<group name="admin" macro="str2datetime">
% Administrative Contacts:{{ _start_ }}
% ===========
person:           {{ name | ORPHRASE }}
person-loc:       {{ name_local | ORPHRASE }}
organization-loc: {{ organization_local | ORPHRASE }}
e-mail:           {{ email | ORPHRASE }}
address:          {{ address | ORPHRASE | joinmatches(", ") }}
address-loc:      {{ address | ORPHRASE | joinmatches(", ") }}
address-loc:      {{ address | ORPHRASE | joinmatches(", ") }}
address-loc:      {{ address | ORPHRASE | joinmatches(", ") }}
postal-code-loc:  {{ zip_code | ORPHRASE }}
country-loc:      {{ country | ORPHRASE }}
phone:            {{ phone }}
fax:              {{ fax }}
status:           {{ status | to_list | joinmatches }}
created:          {{ created | ORPHRASE }}
source:           UAEPP
</group>
</group>


<output macro="unpack" />
