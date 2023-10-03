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
            ).replace(tzinfo=pytz.timezone(country_timezones['no'][0]))

    # 有効期限
    if 'expiration' in data:
        if type(data['expiration']) == str:
            data['expiration'] = datetime.datetime.strptime(
                data['expiration'],
                '%Y-%m-%d'
            ).replace(tzinfo=pytz.timezone(country_timezones['no'][0]))

    # 最終更新
    if 'updated' in data:
        if type(data['updated']) == str:
            data['updated'] = datetime.datetime.strptime(
                data['updated'],
                '%Y-%m-%d'
            ).replace(tzinfo=pytz.timezone(country_timezones['no'][0]))

    return data

</macro>


## Template
## =======================================================

% By looking up information in the domain registration directory
% service, you confirm that you accept the terms and conditions of the
% service:
% https://www.norid.no/en/domeneoppslag/vilkar/
%
% Norid AS holds the copyright to the lookup service, content,
% layout and the underlying collections of information used in the
% service (cf. the Act on Intellectual Property of May 2, 1961, No.
% 2). Any commercial use of information from the service, including
% targeted marketing, is prohibited. Using information from the domain
% registration directory service in violation of the terms and
% conditions may result in legal prosecution.
%
% The whois service at port 43 is intended to contribute to resolving
% technical problems where individual domains threaten the
% functionality, security and stability of other domains or the
% internet as an infrastructure. It does not give any information
% about who the holder of a domain is. To find information about a
% domain holder, please visit our website:
% https://www.norid.no/en/domeneoppslag/

<group macro="str2datetime">
{{ ignore }}omain Information

Domain Name................: {{ domain_name }}
DNSSEC.....................: {{ dnssec | lower }}

Additional information:
Created:         {{ created }}
Last updated:    {{ updated }}
</group>
