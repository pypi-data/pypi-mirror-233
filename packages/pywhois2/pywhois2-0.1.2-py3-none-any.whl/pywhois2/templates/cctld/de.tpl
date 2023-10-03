## Copyright (c) 2023 Blacknon. All rights reserved.
## Use of this source code is governed by an MIT license
## that can be found in the LICENSE file.
## =======================================================

## Macro
## =======================================================



## Template
## =======================================================


% Restricted rights.
%
% Terms and Conditions of Use
%
% The above data may only be used within the scope of technical or
% administrative necessities of Internet operation or to remedy legal
% problems.
% The use for other purposes, in particular for advertising, is not permitted.
%
% The DENIC whois service on port 43 doesn't disclose any information concerning
% the domain holder, general request and abuse contact.
% This information can be obtained through use of our web-based whois service
% available at the DENIC website:
% http://www.denic.de/en/domains/whois-service/web-whois.html
%
%

<group>
Domain: {{ domain_names }}
Nserver: {{ name_servers | lower | ORPHRASE | to_list | joinmatches }}
Dnskey: {{ dns_keys | ORPHRASE | to_list | joinmatches }}
Status: {{ status }}
Changed: {{ updated }}
</group>
