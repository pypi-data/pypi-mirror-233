## Copyright (c) 2023 Blacknon. All rights reserved.
## Use of this source code is governed by an MIT license
## that can be found in the LICENSE file.
## =======================================================

## Macro
## =======================================================

<macro>
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

<group macro="str2datetime">
Domain Name: {{ domain_name | lower | ORPHRASE }}
Registry Domain ID: {{ registry_domain_id | lower }}
Registry WHOIS Server: {{ registrar_whois_server | lower }}
Updated Date: {{ updated | ORPHRASE }}
Creation Date: {{ created | ORPHRASE }}
Registry Expiry Date: {{ expiration | ORPHRASE }}
Registrar: {{ registrar_name | ORPHRASE }}
Registrar Abuse Contact Email: {{ registrar_email }}
Registrar Abuse Contact Phone: {{ registrar_phone }}
Registry RegistrantID: {{ registrant_id | ORPHRASE }}
RegistrantName: {{ registrant_name | ORPHRASE }}
RegistrantOrganization: {{ registrant_organization | ORPHRASE }}
RegistrantStreet: {{ registrant_address | ORPHRASE | joinmatches(", ") }}
RegistrantCity: {{ registrant_address | ORPHRASE | joinmatches(", ") }}
RegistrantState/Province: {{ registrant_address | ORPHRASE | joinmatches(", ") }}
RegistrantPostal Code: {{ registrant_zip_code | ORPHRASE }}
RegistrantCountry: {{ registrant_country | ORPHRASE }}
RegistrantPhone: {{ registrant_phone | ORPHRASE }}
RegistrantFax: {{ registrant_fax | ORPHRASE }}
RegistrantEmail: {{ registrant_email | ORPHRASE }}
Registry AdminID: {{ admin_id | ORPHRASE }}
AdminName: {{ admin_name | ORPHRASE }}
AdminOrganization: {{ admin_organization | ORPHRASE }}
AdminStreet: {{ admin_address | ORPHRASE | joinmatches(", ") }}
AdminCity: {{ admin_address | ORPHRASE | joinmatches(", ") }}
AdminState/Province: {{ admin_address | ORPHRASE | joinmatches(", ") }}
AdminPostal Code: {{ admin_zip_code | ORPHRASE }}
AdminCountry: {{ admin_country | ORPHRASE }}
AdminPhone: {{ admin_phone | ORPHRASE }}
AdminFax: {{ admin_fax | ORPHRASE }}
AdminEmail: {{ admin_email | ORPHRASE }}
Registry TechID: {{ tech_id | ORPHRASE }}
TechName: {{ tech_name | ORPHRASE }}
TechOrganization: {{ tech_organization | ORPHRASE }}
TechStreet: {{ tech_address | ORPHRASE | joinmatches(", ") }}
TechCity: {{ tech_address | ORPHRASE | joinmatches(", ") }}
TechState/Province: {{ tech_address | ORPHRASE | joinmatches(", ") }}
TechPostal Code: {{ tech_zip_code | ORPHRASE }}
TechCountry: {{ tech_country | ORPHRASE }}
TechPhone: {{ tech_phone | ORPHRASE }}
TechFax: {{ tech_fax | ORPHRASE }}
TechEmail: {{ tech_email | ORPHRASE }}
Registry BillingID: {{ billing_id | ORPHRASE }}
BillingName: {{ billing_name | ORPHRASE }}
BillingOrganization: {{ billing_organization | ORPHRASE }}
BillingStreet: {{ billing_address | ORPHRASE | joinmatches(", ") }}
BillingCity: {{ billing_address | ORPHRASE | joinmatches(", ") }}
BillingState/Province: {{ billing_address | ORPHRASE | joinmatches(", ") }}
BillingPostal Code: {{ billing_zip_code | ORPHRASE }}
BillingCountry: {{ billing_country | ORPHRASE }}
BillingPhone: {{ billing_phone | ORPHRASE }}
BillingFax: {{ billing_fax | ORPHRASE }}
BillingEmail: {{ billing_email | ORPHRASE }}
Name Server: {{ name_servers | ORPHRASE | to_list | joinmatches }}
DNSSEC: {{ dnssec | ORPHRASE }}
</group>
