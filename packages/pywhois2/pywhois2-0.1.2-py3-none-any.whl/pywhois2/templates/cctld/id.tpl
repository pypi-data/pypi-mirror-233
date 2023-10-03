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
            ).replace(tzinfo=pytz.timezone(country_timezones['id'][0]))

    # 有効期限
    if 'expiration' in data:
        if type(data['expiration']) == str:
            data['expiration'] = datetime.datetime.strptime(
                data['expiration'],
                '%Y-%m-%d %H:%M:%S'
            ).replace(tzinfo=pytz.timezone(country_timezones['id'][0]))

    # 最終更新
    if 'updated' in data:
        if type(data['updated']) == str:
            data['updated'] = datetime.datetime.strptime(
                data['updated'],
                '%Y-%m-%d %H:%M:%S'
            ).replace(tzinfo=pytz.timezone(country_timezones['id'][0]))

    return data

def standardize_status(data):
    from stringcase import pascalcase, snakecase
    if 'status' in data:
        if type(data['status']) == list:
            extract_data = data['status']
            del data['status']
            data['status'] = {}

            for d in extract_data:
                data['status'][snakecase(d.lstrip())] = True

    return data

</macro>


## Template
## =======================================================

ID ccTLD whois server
Please see 'whois -h whois.id help' for usage.

<group macro="str2datetime, standardize_status">
Domain ID: {{ domain_id }}
Domain Name: {{ domain_name }}
Created On: {{ created | ORPHRASE }}
Last Updated On: {{ updated | ORPHRASE }}
Expiration Date: {{ expiration | ORPHRASE }}
Status: {{ status | to_list | joinmatches }}

====================================================
Sponsoring Registrar Organization: {{ registrar_name | ORPHRASE }}
Sponsoring Registrar URL: {{ registrar_url }}
Sponsoring Registrar Street: {{ registrar_address |  ORPHRASE | joinmatches(", ") }}
Sponsoring Registrar City: Jakarta {{ registrar_address |  ORPHRASE | joinmatches(", ") }}
Sponsoring Registrar State/Province: {{ registrar_address |  ORPHRASE | joinmatches(", ") }}
Sponsoring Registrar Postal Code: {{ registrar_zip_code }}
Sponsoring Registrar Country: {{ registrar_country }}
Sponsoring Registrar Phone: {{ registrar_phone }}
Sponsoring Registrar Email: {{ registrar_email }}
Name Server: {{ name_servers | lower | ORPHRASE | to_list | joinmatches }}
DNSSEC: {{ dnssec | ORPHRASE }}
</group>

Abuse Domain Report https://pandi.id/domain-abuse-form/?lang=en
For more information on Whois status codes, please visit https://www.icann.org/resources/pages/epp-status-codes-2014-06-16-en
