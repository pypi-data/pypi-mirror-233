## Copyright (c) 2023 Blacknon. All rights reserved.
## Use of this source code is governed by an MIT license
## that can be found in the LICENSE file.
## =======================================================

## Macro
## =======================================================

<macro>
def domain_name2parent(data):
    if 'domain_name' in data:
        extract_data = data['domain_name']['domain_name']
        if type(extract_data) == str:
            del data['domain_name']
            data['domain_name'] = extract_data

    return data

def status2parent(data):
    from stringcase import pascalcase, snakecase
    if 'status' in data:
        extract_data = data['status']['status']
        if type(extract_data) == list:
            del data['status']['status']

            data['status'] = {}
            for d in extract_data:
                key = snakecase(d.lstrip().lower())
                if key == "active":
                    key = 'ok'
                data['status'][key] = True

    return data

def registrant_name2parent(data):
    if 'registrant_name' in data:
        extract_data = data['registrant_name']
        if type(extract_data) == dict:
            del data['registrant_name']
            data['registrant_name'] = extract_data['registrant_name']
    return data

def registrar_name2parent(data):
    if 'registrar_name' in data:
        extract_data = data['registrar_name']
        if type(extract_data) == dict:
            del data['registrar_name']
            data['registrar_name'] = extract_data['registrar_name']
            data['registrar_url'] = extract_data['registrar_url']

    return data

def name_servers2parent(data):
    if 'name_servers' in data:
        extract_data = data['name_servers']['name_servers']
        if type(extract_data) == list:
            del data['name_servers']
            data['name_servers'] = extract_data

    return data

def created_parse(data):
    import datetime
    import pytz
    from pytz import country_timezones

    if 'created' in data:
        extract_data = data['created']['created']
        del data['created']

        extract_data_split = extract_data.split(" ")
        day = extract_data_split[0][:2]
        extract_data_split[0] = day
        extract_data = " ".join(extract_data_split)

        data['created'] = datetime.datetime.strptime(
            "{0}{1}".format(extract_data,"000"),
            '%d %B %Y at %H:%M:%S.%f'
        ).replace(tzinfo=pytz.timezone(country_timezones['as'][0]))

    return data

</macro>


## Template
## =======================================================

<group macro="domain_name2parent, status2parent, registrant_name2parent, registrar_name2parent, name_servers2parent, created_parse" del="__ignore_whois__, __ignore_year__, __ignore_date__">
%%% start %%% {{ __ignore_whois__ }} %%% start %%%

<group name="domain_name">
Domain:{{ _start_ }}
     {{ domain_name | strip(' ') | ORPHRASE }}
</group>

<group name="status">
Domain Status:{{ _start_ }}
     {{ status | strip(' ') | ORPHRASE | to_list | joinmatches }}
</group>

<group name="registrant_name">
Registrant:{{ _start_ }}
     {{ registrant_name | ORPHRASE }}
</group>

<group name="registrar_name">
Registrar:{{ _start_ }}
     {{ registrar_name | ORPHRASE }} ({{ registrar_url }})
</group>

<group name="created">
Relevant dates:{{ _start_ }}
     Registered on {{ created | ORPHRASE }}
</group>

<group name="registration_status_group">
Registration status:{{ _start_ }}
     {{ registration_status | ORPHRASE }}
</group>

<group name="name_servers">
Name servers:{{ _start_ }}
     {{ name_servers | ORPHRASE | to_list | joinmatches }}
</group>


WHOIS lookup made on {{ __ignore_date__ }}
This WHOIS information is provided for free by CIDR, operator of
the backend registry for domain names ending in GG, JE, and AS.

Copyright (c) and database right AS Domain Registry 1997 - {{ __ignore_year__ }}.

You may not access this WHOIS server or use any data from it except
as permitted by our Terms and Conditions which are published
at http://www.channelisles.net/legal/whoisterms

They include restrictions and prohibitions on

- using or re-using the data for advertising;
- using or re-using the service for commercial purposes without a licence;
- repackaging, recompilation, redistribution or reuse;
- obscuring, removing or hiding any or all of this notice;
- exceeding query rate or volume limits.

The data is provided on an 'as-is' basis and may lag behind the
register. Access may be withdrawn or restricted at any time.

%%% end %%% {{ __ignore_whois__ }} %%% end %%%
</group>
