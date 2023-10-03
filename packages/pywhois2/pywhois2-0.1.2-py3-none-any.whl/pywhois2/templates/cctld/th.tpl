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
                '%d %b %Y'
            ).replace(tzinfo=pytz.timezone(country_timezones['th'][0]))

    # 有効期限
    if 'expiration' in data:
        if type(data['expiration']) == str:
            data['expiration'] = datetime.datetime.strptime(
                data['expiration'],
                '%d %b %Y'
            ).replace(tzinfo=pytz.timezone(country_timezones['th'][0]))

    # 最終更新
    if 'updated' in data:
        if type(data['updated']) == str:
            data['updated'] = datetime.datetime.strptime(
                data['updated'],
                '%d %b %Y'
            ).replace(tzinfo=pytz.timezone(country_timezones['th'][0]))

    return data

def status2parent(data):
    from stringcase import pascalcase, snakecase
    if 'status' in data:
        extract_data = data['status']
        if type(extract_data) == str:
            del data['status']
            data['status'] = {}
            for line in extract_data.split(" "):
                data['status'][snakecase(line.lstrip())] = True
    return data
</macro>



## Template
## =======================================================

Whois Server Version 2.1.7

<group macro="str2datetime, status2parent">
Domain Name:                {{ domain_name | lower }}
Registrar:                  THNIC
Name Server:                {{ name_servers | lower | ORPHRASE | to_list | joinmatches }}
DNSSEC:                     {{ dnssec }}
Status:                     {{ status | lower }}
Updated date:               {{ updated | ORPHRASE }}
Created date:               {{ created | ORPHRASE }}
Exp date:                   {{ expiration | ORPHRASE }}
Domain Holder Organization: {{ registrant_organization | ORPHRASE }} ({{ registrant_organization_local | ORPHRASE }})
Domain Holder Street:       {{ registrant_address | ORPHRASE }}
Domain Holder Country:      {{ registrant_country }}

Tech Contact:               {{ tech_name | ORPHRASE }}
Tech Organization:          {{ tech_organization | ORPHRASE }}
Tech Street:                {{ tech_address | ORPHRASE }}
Tech Country:               {{ tech_country | ORPHRASE }}
</group>
