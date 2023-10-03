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

    data = registrant2parent(data)
    data = registrar2parent(data)
    data = str2datetime(data)

    return data


def registrant2parent(data):
    if 'registrant' in data:
        extract_data = data['registrant']
        if type(extract_data) == dict:
            del data['registrant']

            for d in extract_data:
                data[d] = extract_data[d]
    return data

def registrar2parent(data):
    if 'registrar' in data:
        extract_data = data['registrar']
        if type(extract_data) == dict:
            del data['registrar']

            for d in extract_data:
                data[d] = extract_data[d]
    return data

def str2datetime(data):
    import datetime
    import pytz
    from pytz import country_timezones

    format = '%d.%m.%Y'
    if 'created' in data:
        data['created'] = datetime.datetime.strptime(
            data['created'],
            format
        ).replace(tzinfo=pytz.timezone(country_timezones['ax'][0]))

    if 'expiration' in data:
        data['expiration'] = datetime.datetime.strptime(
            data['expiration'],
            format
        ).replace(tzinfo=pytz.timezone(country_timezones['ax'][0]))

    if 'available' in data:
        data['available'] = datetime.datetime.strptime(
            data['available'],
            format
        ).replace(tzinfo=pytz.timezone(country_timezones['ax'][0]))

    if 'updated' in data:
        data['updated'] = datetime.datetime.strptime(
            data['updated'],
            format
        ).replace(tzinfo=pytz.timezone(country_timezones['ax'][0]))

    return data
</macro>



## Template
## =======================================================

<group>

domain...............: {{ domain_name }}
status...............: {{ status }}
created..............: {{ created }}
expires..............: {{ expiration }}
available............: {{ available }}
modified.............: {{ updated }}
RegistryLock.........: {{ registry_lock }}

Nameservers

nserver..............: {{ name_servers | lower | ORPHRASE | to_list | joinmatches }}

<group name="registrant">
Holder
{{ _start_ }}
name.................: {{ registrant_name | ORPHRASE }}
register number......: {{ registrant_id }}
address..............: {{ registrant_address | ORPHRASE | joinmatches(", ") }}
country..............: {{ registrant_country }}
phone................: {{ registrant_phone | ORPHRASE }}
holder email.........: {{ registrant_email | ORPHRASE }}
{{ _end_ }}
</group>

<group name="registrar">
Registrar

registrar............: {{ registrar_name | ORPHRASE }}
www..................: {{ registrar_url | ORPHRASE }}
</group>

</group>


<output macro="unpack"/>
