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

    # 登録年月日
    if 'created' in data:
        if type(data['created']) == str:
            data['created'] = datetime.datetime.strptime(
                data['created'],
                '%Y-%m-%d %H:%M:%S'
            ).replace(tzinfo=pytz.timezone(country_timezones['st'][0]))

    # 有効期限
    if 'expiration' in data:
        if type(data['expiration']) == str:
            data['expiration'] = datetime.datetime.strptime(
                data['expiration'],
                '%Y-%m-%d %H:%M:%S'
            ).replace(tzinfo=pytz.timezone(country_timezones['st'][0]))

    # 最終更新
    if 'updated' in data:
        if type(data['updated']) == str:
            data['updated'] = datetime.datetime.strptime(
                data['updated'],
                '%Y-%m-%d %H:%M:%S'
            ).replace(tzinfo=pytz.timezone(country_timezones['st'][0]))

    return data
</macro>


## Template
## =======================================================

Whois Server Version 3.2.2

.ST domains can now be registered with many different competing registrars. Go to http://www.registry.st/registrars for detailed information.

The data in the ST Registry WHOIS database is provided by The Domain Council of
Sao Tome and Principe for information purposes.

The ST Registry does not guarantee its accuracy.

The data in the WHOIS database is protected by copyright.

By submitting a WHOIS query, you agree that you will use this data according with
the terms and policy that is publicly available on http://www.nic.st/terms_of_service
and that you under no circumstances will use this data to allow, enable, or
otherwise support the transmission of mass unsolicited commercial advertising or
solicitations via e-mail (spam).

The Domain Council of Sao Tome reserves the right to modify these terms at any time.

<group macro="str2datetime">
DOMAIN: {{ domain_name }}

REGISTRATION-SERVICE-PROVIDER: {{ registrar_name | ORPHRASE }}.
URL: {{ registrar_url }}

created-date:    {{ created | ORPHRASE }}
updated-date:    {{ updated | ORPHRASE }}
expiration-date: {{ expiration | ORPHRASE }}

registrant-organization: {{ registrant_organization | ORPHRASE }}
registrant-name:         {{ registrant_name | ORPHRASE }}
registrant-street:       {{ registrant_address | ORPHRASE | joinmatches(", ") }}
registrant-city:         {{ registrant_address | ORPHRASE | joinmatches(", ") }}
registrant-state:        {{ registrant_address | ORPHRASE | joinmatches(", ") }}
registrant-zip:          {{ registrant_zip_code | ORPHRASE | }}
registrant-country:      {{ registrant_country }}
registrant-phone:        {{ registrant_phone | ORPHRASE }}
registrant-fax:          {{ registrant_fax | ORPHRASE }}
registrant-email:        {{ registrant_email | ORPHRASE }}

admin-organization: {{ admin_organization | ORPHRASE }}
admin-name:         {{ admin_name | ORPHRASE }}
admin-street:       {{ admin_address | ORPHRASE | joinmatches(", ") }}
admin-city:         {{ admin_address | ORPHRASE | joinmatches(", ") }}
admin-state:        {{ admin_address | ORPHRASE | joinmatches(", ") }}
admin-zip:          {{ admin_zip_code | ORPHRASE | }}
admin-country:      {{ admin_country }}
admin-phone:        {{ admin_phone | ORPHRASE }}
admin-fax:          {{ admin_fax | ORPHRASE }}
admin-email:        {{ admin_email | ORPHRASE }}

tech-organization: {{ tech_organization | ORPHRASE }}
tech-name:         {{ tech_name | ORPHRASE }}
tech-street:       {{ tech_address | ORPHRASE | joinmatches(", ") }}
tech-city:         {{ tech_address | ORPHRASE | joinmatches(", ") }}
tech-state:        {{ tech_address | ORPHRASE | joinmatches(", ") }}
tech-zip:          {{ tech_zip_code | ORPHRASE | }}
tech-country:      {{ tech_country }}
tech-phone:        {{ tech_phone | ORPHRASE }}
tech-fax:          {{ tech_fax | ORPHRASE }}
tech-email:        {{ tech_email | ORPHRASE }}

billing-organization: {{ billing_organization | ORPHRASE }}
billing-name:         {{ billing_name | ORPHRASE }}
billing-street:       {{ billing_address | ORPHRASE | joinmatches(", ") }}
billing-city:         {{ billing_address | ORPHRASE | joinmatches(", ") }}
billing-state:        {{ billing_address | ORPHRASE | joinmatches(", ") }}
billing-zip:          {{ billing_zip_code | ORPHRASE | }}
billing-country:      {{ billing_country }}
billing-phone:        {{ billing_phone | ORPHRASE }}
billing-fax:          {{ billing_fax | ORPHRASE }}
billing-email:        {{ billing_email | ORPHRASE }}

nameserver: {{ name_servers | lower | ORPHRASE | to_list | joinmatches }}
</group>
