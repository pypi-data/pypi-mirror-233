## Copyright (c) 2023 Blacknon. All rights reserved.
## Use of this source code is governed by an MIT license
## that can be found in the LICENSE file.
## =======================================================

## Macro
## =======================================================

<macro>
def standardize_status(data):
    from stringcase import pascalcase, snakecase
    if 'status' in data:
        if type(data['status']) == str:
            extract_data = data['status']
            del data['status']
            data['status'] = {}

            for d in extract_data.split(","):
                data['status'][snakecase(d.lstrip())] = True

    return data

def str2datetime(data):
    import datetime
    import pytz
    from pytz import country_timezones

    # 登録年月日
    if 'created' in data:
        if type(data['created']) == str:
            data['created'] = datetime.datetime.strptime(
                data['created'],
                '%Y-%m-%d'
            ).replace(tzinfo=pytz.timezone(country_timezones['ug'][0]))

    # 有効期限
    if 'expiration' in data:
        if type(data['expiration']) == str:
            data['expiration'] = datetime.datetime.strptime(
                data['expiration'],
                '%Y-%m-%d'
            ).replace(tzinfo=pytz.timezone(country_timezones['ug'][0]))

    # 最終更新
    if 'updated' in data:
        if type(data['updated']) == str:
            data['updated'] = datetime.datetime.strptime(
                data['updated'],
                '%Y-%m-%d'
            ).replace(tzinfo=pytz.timezone(country_timezones['ug'][0]))

    if 'renewed' in data:
        if type(data['renewed']) == str:
            data['renewed'] = datetime.datetime.strptime(
                data['renewed'],
                '%Y-%m-%d'
            ).replace(tzinfo=pytz.timezone(country_timezones['ug'][0]))

    return data
</macro>


## Template
## =======================================================

**********************************************************
*            The UG ccTLD Registry Database              *
**********************************************************

<group macro="standardize_status, str2datetime">
Domain name:                    {{ domain_name }}
Status:                         {{ status | lower }}
Expires On:                     {{ expiration }}
Registered On:                  {{ created }}
Renewed On:                     {{ renewed }}
Nameserver:                     {{ name_servers | strip(' ') | ORPHRASE | to_list | joinmatches }}

Registrant Contact Information:
Registrant Name:                {{ registrant_name | ORPHRASE }}
Registrant Organization:        {{ registrant_organization | ORPHRASE }}
Registrant Country:             {{ registrant_country | ORPHRASE }}
Registrant State / Province:    {{ registrant_address | ORPHRASE | joinmatches(", ") }}
Registrant City:                {{ registrant_address | ORPHRASE | joinmatches(", ") }}
Registrant Address:             {{ registrant_address | ORPHRASE | joinmatches(", ") }}
Registrant Postal Code:         {{ registrant_zip_code | ORPHRASE }}
Registrant Phone:               {{ registrant_phone | ORPHRASE }}
Registrant Email:               {{ registrant_email | ORPHRASE }}

Administrative Contact Information:
Admin Name:                     {{ admin_name | ORPHRASE }}
Admin Organization:             {{ admin_organization | ORPHRASE }}
Admin Country:                  {{ admin_country | ORPHRASE }}
Admin State / Province:         {{ admin_address | ORPHRASE | joinmatches(", ") }}
Admin City:                     {{ admin_address | ORPHRASE | joinmatches(", ") }}
Admin Address:                  {{ admin_address | ORPHRASE | joinmatches(", ") }}
Admin Postal Code:              {{ admin_zip_code | ORPHRASE }}
Admin Phone:                    {{ admin_phone | ORPHRASE }}
Admin Email:                    {{ admin_email | ORPHRASE }}

Technical Contact Information:
Tech Name:                      {{ tech_name | ORPHRASE }}
Tech Organization:              {{ tech_organization | ORPHRASE }}
Tech Country:                   {{ tech_country | ORPHRASE }}
Tech State / Province:          {{ tech_address | ORPHRASE | joinmatches(", ") }}
Tech City:                      {{ tech_address | ORPHRASE | joinmatches(", ") }}
Tech Address:                   {{ tech_address | ORPHRASE | joinmatches(", ") }}
Tech Postal Code:               {{ tech_zip_code | ORPHRASE }}
Tech Phone:                     {{ tech_phone | ORPHRASE }}
Tech Email:                     {{ tech_email | ORPHRASE }}

</group>
