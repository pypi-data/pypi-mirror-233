## Copyright (c) 2023 Blacknon. All rights reserved.
## Use of this source code is governed by an MIT license
## that can be found in the LICENSE file.
## =======================================================

## Macro
## =======================================================

<macro>
def status2parent(data):
    from stringcase import pascalcase, snakecase
    if 'status' in data:
        extract_data = data['status']
        if type(extract_data) == list:
            del data['status']
            data['status'] = {}
            for line in extract_data:
                data['status'][line.lstrip().lower()] = True
    return data

def update_name_servers(data):
    if 'name_servers' in data:
        name_servers = []
        for n in data['name_servers']:
            name_servers.append(n.split(" ")[0])
        data['name_servers'] = name_servers

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
            ).replace(tzinfo=pytz.timezone(country_timezones['nu'][0]))

    # 有効期限
    if 'expiration' in data:
        if type(data['expiration']) == str:
            data['expiration'] = datetime.datetime.strptime(
                data['expiration'],
                '%Y-%m-%d'
            ).replace(tzinfo=pytz.timezone(country_timezones['nu'][0]))

    # 最終更新
    if 'updated' in data:
        if type(data['updated']) == str:
            data['updated'] = datetime.datetime.strptime(
                data['updated'],
                '%Y-%m-%d'
            ).replace(tzinfo=pytz.timezone(country_timezones['nu'][0]))

    return data

</macro>

## Template
## =======================================================

# Copyright (c) 1997- The Swedish Internet Foundation.
# All rights reserved.
# The information obtained through searches, or otherwise, is protected
# by the Swedish Copyright Act (1960:729) and international conventions.
# It is also subject to database protection according to the Swedish
# Copyright Act.
# Any use of this material to target advertising or
# similar activities is forbidden and will be prosecuted.
# If any of the information below is transferred to a third
# party, it must be done in its entirety. This server must
# not be used as a backend for a search engine.
# Result of search for registered domain names under
# the .se top level domain.
# This whois printout is printed with UTF-8 encoding.
#

<group macro="status2parent, update_name_servers, str2datetime">
state:            {{ status | to_list | joinmatches }}
domain:           {{ domain_name }}
holder:           {{ registrant_id }}
created:          {{ created }}
modified:         {{ updated }}
expires:          {{ expiration }}
nserver:          {{ name_servers | lower | ORPHRASE | to_list | joinmatches }}
dnssec:           {{ dnssec }}
registry-lock:    {{ status | to_list | joinmatches }}
status:           {{ status | to_list | joinmatches }}
registrar:        {{ registrar_name | ORPHRASE }}
</group>
