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

    # 有効期限
    if 'expiration' in data:
        if type(data['expiration']) == str:
            data['expiration'] = datetime.datetime.strptime(
                data['expiration'],
                '%d/%m/%Y %H:%M:%S'
            ).replace(tzinfo=pytz.timezone(country_timezones['im'][0]))

    return data
</macro>


## Template
## =======================================================


                This information has been redacted to comply with European Union General Data Protection Regulations (GDPR). Please contact us at info@nic.im if you have any further queries.

<group macro="str2datetime">
Domain Name:	{{ domain_name }}
Domain Managers
Name: Redacted
Address
Redacted
Domain Owners / Registrant
Name: Redacted
Address
Redacted
Administrative Contact
Name: Redacted
Address
Redacted
Billing Contact
Name: Redacted
Address
Redacted
Technical Contact
Name: Redacted
Address
Redacted
Domain Details
Expiry Date: {{ expiration | ORPHRASE }}
Name Server:{{ name_servers | lower | ORPHRASE | to_list | joinmatches }}.
</group>
