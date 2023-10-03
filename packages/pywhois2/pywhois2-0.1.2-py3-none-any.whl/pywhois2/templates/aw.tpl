## Copyright (c) 2023 Blacknon. All rights reserved.
## Use of this source code is governed by an MIT license
## that can be found in the LICENSE file.
## =======================================================

## Macro
## =======================================================

<macro>
def registrar_parse(data):
    if 'registrar_name' in data:
        if type(data['registrar_name']) == dict:
            extract_data = data['registrar_name']
            del data['registrar_name']

            data['registrant_address'] = extract_data['line'][0]
            data['registrant_address'] += ", " + extract_data['line'][1]
            data['registrant_address'] += ", " + extract_data['line'][2]
            data['registrant_address'] += ", " + extract_data['line'][3]
            data['registrar_name'] = extract_data['line'][4]

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
            ).replace(tzinfo=pytz.timezone(country_timezones['aw'][0]))

    # 有効期限
    if 'expiration' in data:
        if type(data['expiration']) == str:
            data['expiration'] = datetime.datetime.strptime(
                data['expiration'],
                '%Y-%m-%d'
            ).replace(tzinfo=pytz.timezone(country_timezones['aw'][0]))

    # 最終更新
    if 'updated' in data:
        if type(data['updated']) == str:
            data['updated'] = datetime.datetime.strptime(
                data['updated'],
                '%Y-%m-%d'
            ).replace(tzinfo=pytz.timezone(country_timezones['aw'][0]))

    return data

def name_servers2parent(data):
    if 'name_servers' in data:
        extract_data = data['name_servers']['name_servers']
        if type(extract_data) == list:
            del data['name_servers']
            data['name_servers'] = extract_data

    return data

def status2parent(data):
    from stringcase import pascalcase, snakecase
    if 'status' in data:
        extract_data = data['status']
        if type(extract_data) == str:
            del data['status']

            data['status'] = {}
            for d in extract_data.split(","):
                key = snakecase(d.lstrip().lower())
                if key == "active":
                    key = 'ok'
                data['status'][key] = True

    return data
</macro>


## Template
## =======================================================

<group del="_ignore_" macro="status2parent, registrar_parse, str2datetime, name_servers2parent">
Domain name: {{ domain_name }}
Status:      {{ status }}

<group name="registrar_name">
Registrar:{{ _start_ }}
   {{ line | ORPHRASE | to_list | joinmatches }}
{{ _end_ }}
</group>

Abuse Contact:

Creation Date: {{ created }}

Updated Date: {{ updated }}

DNSSEC:      {{ dnssec }}

<group name="name_servers">
Domain nameservers:{{ _start_ }}
   {{ name_servers | lower | ORPHRASE | to_list | joinmatches }}
{{ _end_ }}
</group>

Record maintained by: {{ _ignore_ | ORPHRASE }}

</group>

Copyright notice
No part of this publication may be reproduced, published, stored in a
retrieval system, or transmitted, in any form or by any means,
electronic, mechanical, recording, or otherwise, without prior
permission of Setar.

Any use of this material for advertising, targeting commercial offers or
similar activities is explicitly forbidden and liable to result in legal
action. Anyone who is aware or suspects that such activities are taking
place is asked to inform Setar in Aruba.
(c) Setar Aruban Copyright Act, protection of authors' rights (Section 10,
subsection 1, clause 1).
