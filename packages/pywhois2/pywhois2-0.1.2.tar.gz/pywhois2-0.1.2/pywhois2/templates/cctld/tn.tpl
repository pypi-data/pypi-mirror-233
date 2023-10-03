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

    data = organization2parent('owner', 'registrant', data)
    data = organization2parent('administrativ', 'admin', data)
    data = organization2parent('technical', 'tech', data)
    data = name_servers2parent(data)
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

def name_servers2parent(data):
    if 'name_servers' in data:
        extract_data = data['name_servers']['name_servers']
        if type(extract_data) == list:
            del data['name_servers']
            data['name_servers'] = extract_data

    return data

def str2datetime(data):
    import datetime
    import pytz
    from pytz import country_timezones

    # 登録年月日
    if 'created' in data:
        if type(data['created']) == str:
            data['created'] = datetime.datetime.strptime(
                data['created'].replace(" GMT+1", " +01:00"),
                '%d-%m-%Y %H:%M:%S %z'
            ).replace(tzinfo=pytz.timezone(country_timezones['tn'][0]))

    # 有効期限
    if 'expiration' in data:
        if type(data['expiration']) == str:
            data['expiration'] = datetime.datetime.strptime(
                data['expiration'].replace(" GMT+1", " +01:00"),
                '%d-%m-%Y %H:%M:%S %z'
            ).replace(tzinfo=pytz.timezone(country_timezones['tn'][0]))

    # 最終更新
    if 'updated' in data:
        if type(data['updated']) == str:
            data['updated'] = datetime.datetime.strptime(
                data['updated'].replace(" GMT+1", " +01:00"),
                '%d-%m-%Y %H:%M:%S %z'
            ).replace(tzinfo=pytz.timezone(country_timezones['tn'][0]))

    return data
</macro>

## Template
## =======================================================

NIC Whois server for cTLDs : .tn , .تونس
All rights reserved
Copyright "Tunisian Internet Agency - https://whois.ati.tn
Supported ccTLDs : .tn , .تونس
Sectorial domains : .com.tn,.ens.tn,.fin.tn,.gov.tn,.ind.tn,.intl.tn,.nat.tn,.net.tn,.org.tn,.info.tn,.perso.tn,.tourism.tn,.mincom.tn

<group>
Domain name.........: {{ domain_name }}
Details:
Creation date.......: {{ created | ORPHRASE }}
Domain status.......: {{ status }}
Registrar...........: {{ registrar_name | ORPHRASE }}

<group name="{{ type }}">
{{ type | lower }} Contact
Name................: {{ name | ORPHRASE | joinmatches(" ") }}
First name..........: {{ name | ORPHRASE | joinmatches(" ") }}
Address.............: {{ address | ORPHRASE | joinmatches(",") }}
address2............: {{ address | ORPHRASE | joinmatches(",") }}
City................: {{ address | ORPHRASE | joinmatches(",") }}
stateProvince.......: {{ address | ORPHRASE | joinmatches(",") }}
Zip code............: {{ zip_code | ORPHRASE }}
Country.............: {{ country | ORPHRASE }}
Phone...............: {{ phone | ORPHRASE }}
Fax.................: {{ fax | ORPHRASE }}
Email...............: {{ email | ORPHRASE }}
</group>

<group name="{{ type }}">
{{ type | lower }} contact
Name................: {{ name | ORPHRASE | joinmatches(" ") }}
First name..........: {{ name | ORPHRASE | joinmatches(" ") }}
Address.............: {{ address | ORPHRASE | joinmatches(",") }}
address2............: {{ address | ORPHRASE | joinmatches(",") }}
City................: {{ address | ORPHRASE | joinmatches(",") }}
stateProvince.......: {{ address | ORPHRASE | joinmatches(",") }}
Zip code............: {{ zip_code | ORPHRASE }}
Country.............: {{ country | ORPHRASE }}
Phone...............: {{ phone | ORPHRASE }}
Fax.................: {{ fax | ORPHRASE }}
Email...............: {{ email | ORPHRASE }}
</group>

dnssec..............: {{ dnssec }}

<group name="name_servers">
DNS servers{{ _start_ }}
Name................: {{ name_servers | lower | ORPHRASE | to_list | joinmatches }}.
{{ _end_ }}
</group>

</group>

<output macro="unpack" />
