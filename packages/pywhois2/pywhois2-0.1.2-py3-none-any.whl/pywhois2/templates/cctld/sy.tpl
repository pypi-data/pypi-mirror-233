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
</macro>


## Template
## =======================================================

<group macro="str2datetime">
Domain Name: {{ domain_name }}
Domain ID: {{ domain_id }}
WHOIS Server: {{ registrar_whois_server | lower }}
Referral URL: {{ registrar_url }}
Updated Date: {{ updated }}
Creation Date: {{ created }}
Registry Expiry Date: {{ expiration }}
Sponsoring Registrar: {{ registrar_name | ORPHRASE }}
Sponsoring Registrar IANA ID: {{ registrar_id | ORPHRASE }}
Domain Status: {{ status }}
Registrant Name: {{ registrant_name | ORPHRASE }}
Registrant Street: {{ registrant_address | ORPHRASE | joinmatches(", ") }}
Registrant City: {{ registrant_address | ORPHRASE | joinmatches(", ") }}
Registrant State/Province: {{ registrant_address | ORPHRASE | joinmatches(", ") }}
Registrant Postal Code: {{ registrant_zip_code | ORPHRASE }}
Registrant Country: {{ registrant_country }}
Registrant Email: {{ registrant_email }}
Billing Name: {{ billing_name | ORPHRASE }}
Billing Street: {{ billing_address | ORPHRASE | joinmatches(", ") }}
Billing City: {{ billing_address | ORPHRASE | joinmatches(", ") }}
Billing State/Province: {{ billing_address | ORPHRASE | joinmatches(", ") }}
Billing Postal Code: {{ billing_zip_code | ORPHRASE }}
Billing Country: {{ billing_country | ORPHRASE }}
Billing Email: {{ billing_email }}
Tech Name: {{ tech_name | ORPHRASE }}
Tech Street: {{ tech_address | ORPHRASE | joinmatches(", ") }}
Tech City: {{ tech_address | ORPHRASE | joinmatches(", ") }}
Tech State/Province: {{ tech_address | ORPHRASE | joinmatches(", ") }}
Tech Postal Code: {{ tech_zip_code | ORPHRASE }}
Tech Country: {{ tech_country | ORPHRASE }}
Tech Email: {{ tech_email }}
Name Server: {{ name_servers | lower | ORPHRASE | to_list | joinmatches }}
DNSSEC: {{ dnssec | ORPHRASE }}
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
