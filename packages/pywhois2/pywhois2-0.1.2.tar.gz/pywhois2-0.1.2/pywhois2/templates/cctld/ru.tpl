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

    if 'paid' in data:
        if type(data['paid']) == str:
            data['paid'] = datetime.datetime.fromisoformat(data['paid'])

    if 'expiration' in data:
        if type(data['expiration']) == str:
            data['expiration'] = datetime.datetime.strptime(
                data['expiration'].replace('+0:00', '+00:00'),
                '%Y-%m-%d'
            ).replace(tzinfo=pytz.timezone(country_timezones['ru'][0]))

    return data

def status2parent(data):
    from stringcase import pascalcase, snakecase
    if 'status' in data:
        extract_data = data['status']
        if type(extract_data) == str:
            del data['status']
            data['status'] = {}
            for line in extract_data.split(", "):
                data['status'][line.lstrip().lower()] = True
    return data

</macro>


## Template
## =======================================================

% TCI Whois Service. Terms of use:
% https://tcinet.ru/documents/whois_ru_rf.pdf (in Russian)
% https://tcinet.ru/documents/whois_su.pdf (in Russian)

<group macro="str2datetime, status2parent">
domain:        {{ domain_name | lower }}
nserver:       {{ name_servers | lower | to_list | joinmatches }}.
state:         {{ status | ORPHRASE }}
org:           {{ registrant_organization | ORPHRASE }}
taxpayer-id:   -
registrar:     {{ registrar_name | ORPHRASE }}
admin-contact: https://www.nic.ru/whois
created:       {{ created }}
paid-till:     {{ paid }}
free-date:     {{ expiration }}
source:        TCI

Last updated on {{ updated }}
</group>
