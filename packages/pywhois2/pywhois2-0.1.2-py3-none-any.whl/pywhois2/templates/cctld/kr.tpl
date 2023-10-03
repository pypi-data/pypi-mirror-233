## Copyright (c) 2023 Blacknon. All rights reserved.
## Use of this source code is governed by an MIT license
## that can be found in the LICENSE file.
## =======================================================

## Macro
## =======================================================

<macro>
def dnssec2only_english(data):
    if 'dnssec' in data:
        if type(data['dnssec']) == list:
            data['dnssec'] = data['dnssec'][-1]
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
                '%Y. %m. %d.'
            ).replace(tzinfo=pytz.timezone(country_timezones['kr'][0]))

    # 有効期限
    if 'expiration' in data:
        if type(data['expiration']) == str:
            data['expiration'] = datetime.datetime.strptime(
                data['expiration'],
                '%Y. %m. %d.'
            ).replace(tzinfo=pytz.timezone(country_timezones['kr'][0]))

    # 最終更新
    if 'updated' in data:
        if type(data['updated']) == str:
            data['updated'] = datetime.datetime.strptime(
                data['updated'],
                '%Y. %m. %d.'
            ).replace(tzinfo=pytz.timezone(country_timezones['kr'][0]))

    return data
</macro>


## Template
## =======================================================

<group macro="str2datetime, dnssec2only_english">
등록인                      : {{ registrant_name_local | ORPHRASE }}
등록인 주소                 : {{ registrant_address_local | ORPHRASE }}

# ENGLISH

Domain Name                 : {{ domain_name }}
Registrant                  : {{ registrant_name | ORPHRASE }}
Registrant Address          : {{ registrant_address | ORPHRASE }}
Registrant Zip Code         : {{ registrant_zip_code | ORPHRASE }}
Administrative Contact(AC)  : {{ admin_name }}
AC E-Mail                   : {{ admin_email }}
AC Phone Number             : {{ admin_phone }}
Registered Date             : {{ created | ORPHRASE }}
Last Updated Date           : {{ updated | ORPHRASE }}
Expiration Date             : {{ expiration | ORPHRASE }}
Publishes                   : {{ publish_status }}
DNSSEC                      : {{ dnssec | ORPHRASE | to_list | joinmatches }}

   Host Name                : {{ name_servers | ORPHRASE | to_list | joinmatches }}

- KISA/KRNIC WHOIS Service -

</group>
