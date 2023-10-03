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
        if type(extract_data) == str:
            del data['status']
            data['status'] = {}
            for line in extract_data.split(","):
                data['status'][line.lstrip().lower()] = True
    return data

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
            ).replace(tzinfo=pytz.timezone(country_timezones['pk'][0]))

    # 有効期限
    if 'expiration' in data:
        if type(data['expiration']) == str:
            data['expiration'] = datetime.datetime.strptime(
                data['expiration'].replace('+0:00', '+00:00'),
                '%Y-%m-%d'
            ).replace(tzinfo=pytz.timezone(country_timezones['pk'][0]))

    # 最終更新
    if 'updated' in data:
        if type(data['updated']) == str:
            data['updated'] = datetime.datetime.strptime(
                data['updated'].replace('+0:00', '+00:00'),
                '%Y-%m-%d'
            ).replace(tzinfo=pytz.timezone(country_timezones['pk'][0]))

    return data
</macro>

## Template
## =======================================================

% The WHOIS service offered by ROTLD and the access to the records in the ROTLD WHOIS database
% are provided for information purposes and to be used within the scope of technical or administrative
% necessities of Internet operation or to remedy legal problems. The use for other purposes,
% in particular for advertising and domain hunting, is not permitted.

% Without prejudice to the above, it is explicitly forbidden to extract, copy and/or use or re-utilise
% in any form and by any means (electronically or not) the whole or a quantitatively or qualitatively
% substantial part of the contents of the WHOIS database without prior and explicit permission by ROTLD,
% nor in any attempt hereof, to apply automated, electronic processes to ROTLD (or its systems).

% ROTLD cannot, under any circumstances, be held liable in case the stored information would prove
% to be wrong, incomplete or not accurate in any sense.

% You agree that any reproduction and/or transmission of data for commercial purposes will always
% be considered as the extraction of a substantial part of the content of the WHOIS database.

% By submitting the query you agree to abide by this policy and accept that ROTLD can take measures
% to limit the use of its WHOIS services in order to protect the privacy of its registrants or the
% integrity of the database.

% The ROTLD WHOIS service on port 43 never discloses any information concerning the registrant.

% Registrant information can be obtained through use of the web-based whois service available from
% the ROTLD website www.rotld.ro

<group macro="str2datetime, status2parent">
  Domain Name: {{ domain_name }}
  Registered On: {{ created | ORPHRASE }}
  Expires On: {{ expiration | ORPHRASE }}
  Registrar: {{ registrar_name | ORPHRASE }}
  Referral URL: {{ registrar_url | ORPHRASE }}

  DNSSEC: {{ dnssec }}

  Nameserver: {{ name_servers | lower | ORPHRASE | to_list | joinmatches }}

  Domain Status: {{ status }}
</group>
