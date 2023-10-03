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
                data['created'].replace('+0:00', '+00:00'),
                '%d-%b-%Y %H:%M:%S UTD'
            ).replace(tzinfo=pytz.timezone(country_timezones['om'][0]))

    # 有効期限
    if 'expiration' in data:
        if type(data['expiration']) == str:
            data['expiration'] = datetime.datetime.strptime(
                data['expiration'].replace('+0:00', '+00:00'),
                '%d-%b-%Y %H:%M:%S %Z'
            ).replace(tzinfo=pytz.timezone(country_timezones['om'][0]))

    # 最終更新
    if 'updated' in data:
        if type(data['updated']) == str:
            data['updated'] = datetime.datetime.strptime(
                data['updated'].replace('+0:00', '+00:00'),
                '%d-%b-%Y %H:%M:%S %Z'
            ).replace(tzinfo=pytz.timezone(country_timezones['om'][0]))

    return data

def status2parent(data):
    from stringcase import pascalcase, snakecase
    if 'status' in data:
        extract_data = data['status']
        if type(extract_data) == str:
            del data['status']
            data['status'] = {}
            for line in extract_data.split(","):
                data['status'][line.lstrip().lower()] = True
    return data
</macro>


## Template
## =======================================================

<group macro="str2datetime, status2parent">
Domain Name:                     {{ domain_name }}
Last Modified:                   {{ updated | ORPHRASE }}
Registrar Name:                  {{ registrar_name | ORPHRASE }}
Status:                          {{ status | ORPHRASE }}

Registrant Contact Name:         {{ registrant_name | ORPHRASE }}
Registrant Contact Email:        {{ registrant_email | ORPHRASE }}
Registrant Contact Organisation: {{ registrant_organization | ORPHRASE }}
Registrant Contact City:         {{ registrant_address | ORPHRASE }}
Registrant Contact Country:      {{ registrant_country }}

Tech Contact Name:               {{ tech_name | ORPHRASE }}
Tech Contact Email:              {{ tech_email | ORPHRASE }}
Tech Contact Organisation:       {{ tech_organization | ORPHRASE }}
Tech Contact City:               {{ tech_address | ORPHRASE }}
Tech Contact Country:            {{ tech_country }}

Name Server:                     {{ name_servers | lower | ORPHRASE | to_list | joinmatches }}
</group>
