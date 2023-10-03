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
                '%Y-%m-%d'
            ).replace(tzinfo=pytz.timezone(country_timezones['lt'][0]))

    # 有効期限
    if 'expiration' in data:
        if type(data['expiration']) == str:
            data['expiration'] = datetime.datetime.strptime(
                data['expiration'].replace('+0:00', '+00:00'),
                '%Y-%m-%d'
            ).replace(tzinfo=pytz.timezone(country_timezones['lt'][0]))

    # 最終更新
    if 'updated' in data:
        if type(data['updated']) == str:
            data['updated'] = datetime.datetime.strptime(
                data['updated'].replace('+0:00', '+00:00'),
                '%Y-%m-%d'
            ).replace(tzinfo=pytz.timezone(country_timezones['lt'][0]))

    return data
</macro>

## Template
## =======================================================

% Hello, this is the DOMREG whois service.
%
% By submitting a query you agree not to use the information made
% available to:
% - allow, enable or otherwise support the transmission of unsolicited,
%   commercial advertising or other solicitations whether via email or
%   otherwise;
% - target advertising in any possible way;
% - to cause nuisance in any possible way to the registrants by sending
%   (whether by automated, electronic processes capable of enabling
%   high volumes or other possible means) messages to them.
%
% Version 0.4
%
% For more information please visit https://whois.lt
%

<group macro="str2datetime">
Domain:			{{ domain_name }}
Status:			{{ status }}
Registered:		{{ created }}
Expires:		{{ expiration }}
%
Registrar:		{{ registrar_name | ORPHRASE }}
Registrar website:	{{ registrar_url }}
Registrar email:	{{ registrar_email }}
%
Contact organization:	{{ contact_organization | ORPHRASE }}
Contact email:		{{ contact_email }}
%
Nameserver:		{{ name_servers | ORPHRASE | to_list | joinmatches }}
</group>
