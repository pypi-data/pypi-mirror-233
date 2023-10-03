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
                data['status'][line.lower()] = True
    return data
</macro>

## Template
## =======================================================

% Access to RESTENA DNS-LU WHOIS information is provided to assist persons
% in determining the content of a domain name registration record in the LU
% registration database. The data in this record is provided by RESTENA DNS-LU
% for information purposes only, and RESTENA DNS-LU does not guarantee its
% accuracy. Compilation, repackaging, dissemination or other use of the
% WHOIS database in its entirety, or of a substantial part thereof, is not
% allowed without the prior written permission of RESTENA DNS-LU.
%
% By submitting a WHOIS query, you agree to abide by this policy. You acknowledge
% that the use of the WHOIS database is regulated by the ACCEPTABLE USE POLICY
% (http://www.dns.lu/en/support/domainname-availability/whois-gateway/), that you are aware of its
% content, and that you accept its terms and conditions.
%
% You agree especially that you will use this data only for lawful purposes and
% that you will not use this data to:
% (1) allow, enable, or otherwise support the transmission of mass unsolicited,
% commercial advertising or solicitations via e-mail (spam); or
% (2) enable high volume, automated, electronic processes that apply to
% RESTENA DNS-LU (or its systems).
%
% All rights reserved.
%

<group macro="status2parent">
domainname:     {{ domain_name }}
domaintype:     {{ status }}
nserver:        {{ name_servers | ORPHRASE | to_list | joinmatches }}
ownertype:      {{ registrant_type }}
org-country:    {{ registrant_country }}
registrar-name:         {{ registrar_name }}
registrar-email:        {{ registrar_email }}
registrar-url:          {{ registrar_url }}
registrar-country:      {{ registrar_country }}
%
% More details on the domain may be available at below whois-web URL.
% Next to possible further data a form to contact domain operator or
% request further details is available.
whois-web:         https://www.dns.lu/en/support/domainname-availability/whois-gateway/

</group>
