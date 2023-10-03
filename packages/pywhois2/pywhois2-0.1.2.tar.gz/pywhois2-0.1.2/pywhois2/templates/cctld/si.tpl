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
                '%Y-%m-%d'
            ).replace(tzinfo=pytz.timezone(country_timezones['si'][0]))

    # 有効期限
    if 'expiration' in data:
        if type(data['expiration']) == str:
            data['expiration'] = datetime.datetime.strptime(
                data['expiration'],
                '%Y-%m-%d'
            ).replace(tzinfo=pytz.timezone(country_timezones['si'][0]))

    # 最終更新
    if 'updated' in data:
        if type(data['updated']) == str:
            data['updated'] = datetime.datetime.strptime(
                data['updated'],
                '%Y-%m-%d'
            ).replace(tzinfo=pytz.timezone(country_timezones['si'][0]))

    return data

</macro>


## Template
## =======================================================

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% This is ARNES whois database
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Rights restricted by copyright.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% The WHOIS service offered by Arnes, .si Registry, is
% provided for information purposes only. It allows persons
% to check whether a specific domain name is still available
% or not and to obtain information related to the registration
% records of existing domain names.
%
% This WHOIS service accepts and displays only ASCII characters.

% By submitting a query to our WHOIS lookup service, you agree
% to the restrictions on the use of WHOIS and WHOIS data as follows:
%      o You may not allow, enable or otherwise support
%        the transmission of unsolicited, commercial advertising
%        or other solicitations, whether via email or otherwise;
%      o You may not use the information to target advertising
%        in any possible way;
%      o You may not cause inconvenience the domain name holders
%        in any possible way by sending them messages
%        (whether by automated, electronic processes capable of
%        enabling high volumes or other possible means);
%      o You may not copy, extract and/or publish contents
%        of the WHOIS database.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

<group macro="str2datetime">
domain:		{{ domain_name }}
registrar:	{{ registrar_name | ORPHRASE }}
registrar-url:	{{ registrar_url | ORPHRASE }}
nameserver:	{{ name_servers | lower | to_list | joinmatches }}
nameserver:	{{ name_servers | lower | to_list | joinmatches }} ({{ ignore | ORPHRASE }})
registrant:	{{ registrant_id }}
status:		{{ status }}
created:	{{ created | ORPHRASE }}
expire:		{{ expiration | ORPHRASE }}
source:		ARNES

Domain holder:
NOT DISCLOSED

Tech:
NOT DISCLOSED
</group>

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Full domain details are available here http://www.registry.si
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
