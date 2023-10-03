## Copyright (c) 2023 Blacknon. All rights reserved.
## Use of this source code is governed by an MIT license
## that can be found in the LICENSE file.
## =======================================================

## Macro
## =======================================================

<macro>
def str2datetime(data):
    import datetime
    import pytz
    from pytz import country_timezones

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

def status2parent(data):
    from stringcase import pascalcase, snakecase
    if 'status' in data:
        extract_data = data['status']
        if type(extract_data) == list:
            del data['status']
            data['status'] = {}
            for line in extract_data:
                data['status'][snakecase(line.lstrip())] = True
    return data
</macro>

## Template
## =======================================================

<group macro="str2datetime, status2parent">
Domain Name: {{ domain_name }}
WHOIS Server: {{ registrar_whois_server | lower }}
Creation Date: {{ created | ORPHRASE }}
Registry Expiry Date: {{ expiration | ORPHRASE }}
Sponsoring Registrar: {{ registrar_name | ORPHRASE }}
Sponsoring Registrar IANA ID: {{ registrar_id | ORPHRASE }}
Domain Status: {{ status | ORPHRASE | to_list | joinmatches }}

Registrant Organization: {{ registrant_organization | ORPHRASE }}.




Name Server: {{ name_servers | lower | ORPHRASE | to_list | joinmatches }}

DNSSEC: {{ dnssec }}

Additional Section
Sponsoring Registrar URL: {{ registrar_url }}
Sponsoring Registrar Address: {{ registrar_address | ORPHRASE | joinmatches(", ") }}
Sponsoring Registrar Country: {{ registrar_country }}
Sponsoring Registrar Phone: {{ registrar_phone | ORPHRASE }}
Sponsoring Registrar Fax: {{ registrar_fax | ORPHRASE }}
Sponsoring Registrar Customer Service Contact: {{ registrar_contact_name | ORPHRASE }}
Sponsoring Registrar Customer Service Email: {{ registrar_contact_email | ORPHRASE }}
Sponsoring Registrar Admin Contact: {{ registrar_admin_name | ORPHRASE }}
Sponsoring Registrar Admin Email: {{ registrar_admin_email | ORPHRASE }}
</group>

The data in the WHOIS database of TC Registry is provided by NICTC Registry LTD for information purposes, and to assist persons in obtaining information about or related to domain name registration records. By submitting a WHOIS query, you agree that you will use this data only for lawful purposes and that, under no circumstances, you will use this data to enable high volume, automated, electronic processes that apply to NICTC Registry or its systems. NIC TC Registry LTD reserves the right to modify these terms.
By submitting this query, you agree to abide by this policy.
