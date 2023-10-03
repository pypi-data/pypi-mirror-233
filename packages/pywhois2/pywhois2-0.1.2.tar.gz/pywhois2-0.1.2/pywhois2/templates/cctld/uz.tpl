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

    data = organization2parent('registrant', 'registrant', data)
    data = organization2parent('administrative', 'admin', data)
    data = organization2parent('technical', 'tech', data)
    data = organization2parent('billing', 'billing', data)
    data = name_servers2parent(data)
    data = str2datetime(data)
    data = standardize_status(data)

    return data

def name_servers2parent(data):
    if 'name_servers' in data:
        extract_data = data['name_servers']['name_servers']
        if type(extract_data) == list:
            del data['name_servers']
            data['name_servers'] = extract_data

    return data

def organization2parent(organization_type , organization_type_name, data):
    if organization_type in data:
        if type(data[organization_type]) == dict:
            extract_data = data[organization_type]['line']
            del data[organization_type]

            data["{0}_{1}".format(organization_type_name,'organization')] = extract_data[0]
            line_2 = extract_data[1].replace(' [at] ', '@').split('(')
            data["{0}_{1}".format(organization_type_name,'name')] = " ".join(line_2[0:-1])
            data["{0}_{1}".format(organization_type_name,'email')] = line_2[-1].replace(')', '')
            data["{0}_{1}".format(organization_type_name,'address')] = ", ".join(extract_data[2:5])
            data["{0}_{1}".format(organization_type_name,'phone')] = " ".join(extract_data[6].split(' ')[1:])
            data["{0}_{1}".format(organization_type_name,'fax')] = " ".join(extract_data[7].split(' ')[1:])

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
                '%d-%b-%Y'
            ).replace(tzinfo=pytz.timezone(country_timezones['uz'][0]))

    # 有効期限
    if 'expiration' in data:
        if type(data['expiration']) == str:
            data['expiration'] = datetime.datetime.strptime(
                data['expiration'],
                '%d-%b-%Y'
            ).replace(tzinfo=pytz.timezone(country_timezones['uz'][0]))

    # 最終更新
    if 'updated' in data:
        if type(data['updated']) == str:
            data['updated'] = datetime.datetime.strptime(
                data['updated'],
                '%d-%b-%Y'
            ).replace(tzinfo=pytz.timezone(country_timezones['uz'][0]))

    return data

def standardize_status(data):
    from stringcase import pascalcase, snakecase
    if 'status' in data:
        if type(data['status']) == str:
            extract_data = data['status']
            del data['status']
            data['status'] = {}

            for d in extract_data.split(","):
                data['status'][snakecase(d.lstrip())] = True

    return data
</macro>


## Template
## =======================================================

% Uzbekistan Whois Server Version 1.0

% Domain names in the .uz domain can now be registered
% with many different competing registrars. Go to http://www.cctld.uz/
% for detailed information.

% NOTICE: The expiration date displayed in this record is the date the
% registrar's sponsorship of the domain name registration in the registry is
% currently set to expire. This date does not necessarily reflect the expiration
% date of the domain name registrant's agreement with the sponsoring
% registrar.  Users may consult the sponsoring registrar's Whois database to
% view the registrar's reported date of expiration for this registration.

% TERMS OF USE: You are not authorized to access or query our Whois
% database through the use of electronic processes that are high-volume and
% automated except as reasonably necessary to register domain names or
% modify existing registrations; the Data in Center UZINFOCOM ccTLD.uz
% Services ( Center UZINFOCOM ) Whois database is provided by Center UZINFOCOM for
% information purposes only, and to assist persons in obtaining information
% about or related to a domain name registration record. Center UZINFOCOM does not
% guarantee its accuracy. By submitting a Whois query, you agree to abide
% by the following terms of use: You agree that you may use this Data only
% for lawful purposes and that under no circumstances will you use this Data
% to: (1) allow, enable, or otherwise support the transmission of mass
% unsolicited, commercial advertising or solicitations via e-mail, telephone,
% or facsimile; or (2) enable high volume, automated, electronic processes
% that apply to Center UZINFOCOM (or its computer systems). The compilation,
% repackaging, dissemination or other use of this Data is expressly
% prohibited without the prior written consent of Center UZINFOCOM. You agree not to
% use electronic processes that are automated and high-volume to access or
% query the Whois database except as reasonably necessary to register
% domain names or modify existing registrations. Center UZINFOCOM reserves the right
% to restrict your access to the Whois database in its sole discretion to ensure
% operational stability. Center UZINFOCOM may restrict or terminate your access to the
% Whois database for failure to abide by these terms of use. Center UZINFOCOM
% reserves the right to modify these terms at any time.

% The Registry database contains ONLY .UZ domains and
% Registrars.

% Registration Service Provided By: Tomas

<group>
Domain Name: {{ domain_name | lower |  ORPHRASE }}

<group name="{{ type }}">
{{ type | lower | resub(' ', '_') }}:
    {{ line | ORPHRASE | to_list | joinmatches }}
</group>

Creation Date: {{ created }}
Expiration Date: {{ expiration }}

<group name="name_servers">
Domain servers in listed order:{{ _start_ }}
    {{ name_servers | ORPHRASE | to_list | joinmatches }}
{{ _end_ }}
</group>

<group name="{{ type }}">
{{ type | lower }} Contact:
    {{ line | ORPHRASE | to_list | joinmatches }}
</group>

Status: {{ status | lower }}
</group>

% The data in this whois database is provided to you for information purposes only, that is, to assist you in obtaining
% information about or related to a domain name registration record. We make this information available "as is", and do
% not guarantee its accuracy. By submitting a whois query, you agree that you will use this data only for lawful
% purposes and that, under no circumstances will you use this data to:(1) enable high volume, automated, electronic
% processes that stress or load this whois database system providing you this information; or(2) allow,  enable, or
% otherwise % support the transmission of mass unsolicited,  commercial advertising or solicitations via direct mail,
% electronic mail, or by telephone. The compilation, repackaging, dissemination or other use of this data is expressly
% prohibited without prior written consent from us. The registrar of record is Critical Internet, Inc.. We reserve the
% right to modifythese terms at any time. By submitting this query, you agree to abideby these terms.


%  The Whois Server (ver. 1.0) of ccTLD.UZ
%  (c) 2023, Center UZINFOCOM

<output macro="unpack" />
