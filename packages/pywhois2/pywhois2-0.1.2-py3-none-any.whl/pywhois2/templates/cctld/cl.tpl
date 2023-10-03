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

    format = '%Y-%m-%d %H:%M:%S'
    if 'created' in data:
        data['created'] = datetime.datetime.strptime(
            data['created'].replace(' CLST',''),
            format
        ).replace(tzinfo=pytz.timezone(country_timezones['cl'][0]))

    if 'updated' in data:
        data['updated'] = datetime.datetime.strptime(
            data['updated'].replace(' CLST',''),
            format
        ).replace(tzinfo=pytz.timezone(country_timezones['cl'][0]))

    if 'expiration' in data:
        data['expiration'] = datetime.datetime.strptime(
            data['expiration'].replace(' CLST',''),
            format
        ).replace(tzinfo=pytz.timezone(country_timezones['cl'][0]))

    return data

</macro>


## Template
## =======================================================

%%
%% This is the NIC Chile Whois server (whois.nic.cl).
%%
%% Rights restricted by copyright.
%% See https://www.nic.cl/normativa/politica-publicacion-de-datos-cl.pdf
%%

<group macro="str2datetime">
Domain name: {{ domain_name | lower | ORPHRASE }}
Registrant name: {{ registrant_name | ORPHRASE }}
Registrant organisation: {{ registrant_organization | ORPHRASE }}
Registrar name: {{ registrar_name | ORPHRASE }}
Registrar URL: {{ registrar_url | ORPHRASE }}
Creation date: {{ created | ORPHRASE }}
Expiration date: {{ expiration | ORPHRASE }}
Name server: {{ name_servers | lower | ORPHRASE | to_list | joinmatches }}
</group>

%%
%% For communication with domain contacts please use website.
%% See https://www.nic.cl/registry/Whois.do?d=google.cl
%%
