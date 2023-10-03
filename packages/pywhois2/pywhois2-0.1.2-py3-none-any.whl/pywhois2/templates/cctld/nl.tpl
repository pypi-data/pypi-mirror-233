## Copyright (c) 2023 Blacknon. All rights reserved.
## Use of this source code is governed by an MIT license
## that can be found in the LICENSE file.
## =======================================================

## Macro
## =======================================================

<macro>
def unpack(data):
    while True:
        if type(data) == list:
            data = data[0]
        else:
            break

    update_data = {}
    for d in data:
        if type(data[d]) == list:
            if type(data[d][0]) == dict:
                data[d] = data[d][0]

        elif type(data[d]) == dict:
            if not data[d]:
                continue
        update_data[d] = data[d]
    data = update_data

    data = reseller_parse(data)
    data = registrar_parse(data)
    data = name_servers2parent(data)
    data = str2datetime(data)

    return data

def reseller_parse(data):
    if 'reseller' in data:
        extract_data = []
        for d in data['reseller']['line']:
            extract_data.append(d.rstrip())
        del data['reseller']

        data['reseller_name'] = extract_data[0]
        data['reseller_address'] = ", ".join(extract_data[1:])
    return data

def registrar_parse(data):
    if 'registrar' in data:
        extract_data = []
        for d in data['registrar']['line']:
            extract_data.append(d.rstrip())
        del data['registrar']

        data['registrar_name'] = extract_data[0]
        data['registrar_address'] = ", ".join(extract_data[1:])
    return data

def name_servers2parent(data):
    if 'name_servers' in data:
        extract_data = data['name_servers']['name_servers']
        if type(extract_data) == list:
            del data['name_servers']
            data['name_servers'] = extract_data

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
            ).replace(tzinfo=pytz.timezone(country_timezones['nl'][0]))

    # 有効期限
    if 'expiration' in data:
        if type(data['expiration']) == str:
            data['expiration'] = datetime.datetime.strptime(
                data['expiration'],
                '%Y-%m-%d'
            ).replace(tzinfo=pytz.timezone(country_timezones['nl'][0]))

    # 最終更新
    if 'updated' in data:
        if type(data['updated']) == str:
            data['updated'] = datetime.datetime.strptime(
                data['updated'],
                '%Y-%m-%d'
            ).replace(tzinfo=pytz.timezone(country_timezones['nl'][0]))

    return data
</macro>


## Template
## =======================================================

<group>
Domain name: {{ domain_name }}
Status:      {{ status }}

<group name="reseller">
Reseller:{{ _start_ }}
   {{ line | _line_ | to_list | joinmatches }}
{{ _end_ }}
</group>

<group name="registrar">
Registrar:{{ _start_ }}
   {{ line | _line_ | to_list | joinmatches }}
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
</group>

Record maintained by: SIDN BV

As the registrant's address is not in the Netherlands, the registrant is
obliged by the General Terms and Conditions for .nl Registrants to use
SIDN's registered office address as a domicile address. More information
on the use of a domicile address may be found at
https://www.sidn.nl/downloads/procedures/Domicile_address.pdf


Copyright notice
No part of this publication may be reproduced, published, stored in a
retrieval system, or transmitted, in any form or by any means,
electronic, mechanical, recording, or otherwise, without prior
permission of SIDN.
These restrictions apply equally to registrars, except in that
reproductions and publications are permitted insofar as they are
reasonable, necessary and solely in the context of the registration
activities referred to in the General Terms and Conditions for .nl
Registrars.
Any use of this material for advertising, targeting commercial offers or
similar activities is explicitly forbidden and liable to result in legal
action. Anyone who is aware or suspects that such activities are taking
place is asked to inform SIDN.
(c) SIDN BV, Dutch Copyright Act, protection of authors' rights
(Section 10, subsection 1, clause 1).


<output macro="unpack" />
