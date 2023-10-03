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
        update_data[d] = data[d]
    data = update_data

    data = registrant_lookup(data)
    data = tech_lookup(data)

    return data

def registrant_lookup(data):
    if 'registrant_hdl' in data:
        if data['registrant_hdl'] in data:
            extract_data = data[data['registrant_hdl']]

            del data[data['registrant_hdl']]
            del data['registrant_hdl']

            for d in extract_data:
                data['registrant_{0}'.format(d)] = extract_data[d]

    return data

def tech_lookup(data):
    if 'tech_hdl' in data:
        postfix = ""
        i = 1
        for d in reversed(data['tech_hdl']):
            if d in data:
                extract_data = data[d]
                del data[d]

                for d in extract_data:
                    data['tech_{0}{1}'.format(d,postfix)] = extract_data[d]

                i += 1
                postfix = "_{0}".format(i)

    return data

def str2datetime(data):
    import datetime
    import pytz
    from pytz import country_timezones

    format = '%Y%m%d %H:%M:%S'
    if 'updated' in data:
        data['updated'] = datetime.datetime.strptime(
            data['updated'],
            format
        ).replace(tzinfo=pytz.timezone(country_timezones['ar'][0]))

    return data

</macro>

## Template
## =======================================================

% Copyright (c)2023 by NIC.AT (1)
%
% Restricted rights.
%
% Except  for  agreed Internet  operational  purposes, no  part  of this
% information  may  be reproduced,  stored  in  a  retrieval  system, or
% transmitted, in  any  form  or by  any means,  electronic, mechanical,
% recording, or otherwise, without prior  permission of NIC.AT on behalf
% of itself and/or the copyright  holders.  Any use of this  material to
% target advertising  or similar activities is explicitly  forbidden and
% can be prosecuted.
%
% It is furthermore strictly forbidden to use the Whois-Database in such
% a  way  that  jeopardizes or  could jeopardize  the  stability  of the
% technical  systems of  NIC.AT  under any circumstances. In particular,
% this includes  any misuse  of the  Whois-Database and  any  use of the
% Whois-Database which disturbs its operation.
%
% Should the  user violate  these points,  NIC.AT reserves  the right to
% deactivate  the  Whois-Database   entirely  or  partly  for  the user.
% Moreover,  the  user  shall be  held liable  for  any  and all  damage
% arising from a violation of these points.

<group macro="str2datetime">
domain:         {{ domain_name }}
registrar:      {{ registrar_name | ORPHRASE }} ( {{ registrar_url }} )
registrant:     {{ registrant_hdl }}
tech-c:         {{ tech_hdl | to_list | joinmatches }}
nserver:        {{ name_servers | ORPHRASE | to_list | joinmatches }}
changed:        {{ updated | ORPHRASE }}
source:         AT-DOM

<group name="{{ nic-hdl }}" macro="str2datetime" del="_hoge_">
{{ _start_ }}
{{ _hoge_ }}ersonname:     {{ name | ORPHRASE }}
organization:   {{ organization | ORPHRASE }}
street address: {{ address | ORPHRASE | joinmatches(", ") }}
postal code:    {{ zip_code | ORPHRASE }}
city:           {{ address | ORPHRASE | joinmatches(", ") }}
country:        {{ country | ORPHRASE }}
phone:          {{ phone }}
fax-no:         {{ fax }}
e-mail:         {{ email }}
nic-hdl:        {{ nic-hdl }}
changed:        {{ updated | ORPHRASE }}
source:         AT-DOM
{{ _end_ }}
</group>

</group>

<output macro="unpack"/>
