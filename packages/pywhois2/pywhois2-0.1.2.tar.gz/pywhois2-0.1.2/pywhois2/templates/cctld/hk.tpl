## Copyright (c) 2023 Blacknon. All rights reserved.
## Use of this source code is governed by an MIT license
## that can be found in the LICENSE file.
## =======================================================

## Macro
## =======================================================

<macro>
def delete_empty_line(data):
    new_data = []
    group_header_line = [
        'Registrant Contact Information:',
        'Administrative Contact Information:',
        'Technical Contact Information:',
        'Name Servers Information:'
    ]

    before_line = ''
    for line in data.splitlines():
        if not before_line in group_header_line:
            new_data.append(line)
        before_line = line
    data = "\n".join(new_data)

    return data

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
    data = organization2parent('admin', 'admin', data)
    data = organization2parent('tech', 'tech', data)
    data = name_servers2parent(data)
    data = str2datetime(data)
    data = registrar_contact_update(data)

    return data

def registrar_contact_update(data):
    if 'registrar_contact' in data:
        rc = data['registrar_contact'].split(' ')
        if len(rc) > 2:
            data['registrar_email'] = rc[1]
            data['registrar_phone'] = " ".join(rc).split(":")[-1]
        else:
            data['registrar_email'] = rc[1]

        del data['registrar_contact']
    return data

def organization2parent(organization_type , organization_type_name, data):
    if organization_type in data:
        if type(data[organization_type]) == dict:
            extract_data = data[organization_type]
            del data[organization_type]

            for d in extract_data:
                data["{0}_{1}".format(organization_type_name,d)] = extract_data[d]
    return data

def address2parent(data):
    if 'address' in data:
        extract_data = data['address']
        if type(extract_data) == dict:
            del data['address']
            data['address'] = extract_data['address']

    return data

def name_servers2parent(data):
    if 'name_servers' in data:
        extract_data = data['name_servers']['name_servers']
        if type(extract_data) == list:
            del data['name_servers']
            data['name_servers'] = extract_data

    return data

def str2datetime(data):
    import datetime
    import pytz
    from pytz import country_timezones

    # 登録年月日
    if 'registrant_created' in data:
        if type(data['registrant_created']) == str:
            data['created'] = datetime.datetime.strptime(
                data['registrant_created'],
                '%d-%m-%Y'
            ).replace(tzinfo=pytz.timezone(country_timezones['hk'][0]))
            del data['registrant_created']

    # 有効期限
    if 'registrant_expiration' in data:
        if type(data['registrant_expiration']) == str:
            data['expiration'] = datetime.datetime.strptime(
                data['registrant_expiration'],
                '%d-%m-%Y'
            ).replace(tzinfo=pytz.timezone(country_timezones['hk'][0]))
            del data['registrant_expiration']

    return data
</macro>


## Template
## =======================================================


<input macro="delete_empty_line" />


 -------------------------------------------------------------------------------
 Whois server by HKIRC
 -------------------------------------------------------------------------------
 .hk top level Domain names can be registered via HKIRC-Accredited Registrars.
 Go to https://www.hkirc.hk/content.jsp?id=280 for details.
 -------------------------------------------------------------------------------


<group macro="name_servers2parent" del="_ignore_">
Domain Name:  {{ domain_name | lower }}
Bundled Domain Name:  {{ registrant_name_local | ORPHRASE }}
Domain Status: {{ status }}

DNSSEC:  {{ dnssec }}

Contract Version:   Refer to registrar

Active variants

Inactive variants

Registrar Name: {{ registrar_name | ORPHRASE }}

Registrar Contact Information: {{ registrar_contact | _line_ }}

Reseller:

<group name='registrant' macro="address2parent">
Registrant Contact Information:{{ _start_ }}
Company English Name (It should be the same as the registered/corporation name on your Business Register Certificate or relevant documents): {{ organization | ORPHRASE }}
Company Chinese name: {{ organization_local | ORPHRASE }}
<group name='address'>
Address:  {{ address | ORPHRASE | joinmatches(', ') }}
{{ address | ORPHRASE | joinmatches(', ') }}
</group>
Country: {{ country | ORPHRASE }}
Phone:  {{ phone | ORPHRASE }}
Fax:  {{ phone | ORPHRASE }}
Email:  {{ email | ORPHRASE }}
Domain Name Commencement Date: {{ created }}
Expiry Date: {{ expiration }}
Re-registration Status:  {{ re_registration_status }}
{{ _end_ }}
</group>


<group name='admin' macro="address2parent">
Administrative Contact Information:{{ _start_ }}
Given name:  {{ name | ORPHRASE | joinmatches(' ') }}
Family name:  {{ name | ORPHRASE | joinmatches(' ') }}
Company name:  {{ organization | ORPHRASE }}
<group name='address'>
Address:  {{ address | ORPHRASE | joinmatches(', ') }}
{{ address | ORPHRASE | joinmatches(', ') }}
</group>
Country: {{ country | ORPHRASE }}
Phone:  {{ phone | ORPHRASE }}
Fax:  {{ phone | ORPHRASE }}
Email:  {{ email | ORPHRASE }}
{{ _end_ }}
</group>

Account Name:  HK9677292T


<group name="tech" macro="address2parent">
Technical Contact Information:{{ _start_ }}
Given name:  {{ name | ORPHRASE | joinmatches(' ') }}
Family name:  {{ name | ORPHRASE | joinmatches(' ') }}
Company name:  {{ organization | ORPHRASE }}
<group name='address'>
Address:  {{ address | ORPHRASE | joinmatches(', ') }}
{{ address | ORPHRASE | joinmatches(', ') }}
</group>
Country: {{ country | ORPHRASE }}
Phone:  {{ phone | ORPHRASE }}
Fax:  {{ phone | ORPHRASE }}
Email:  {{ email | ORPHRASE }}
{{ _end_ }}
</group>

<group name="name_servers" del="_ignore_">
Name Servers Information:{{ _start_ }}
{{ name_servers | ORPHRASE | to_list | joinmatches }}
{{ _end_ }}
</group>

<group name="status_infomation">
Status Information:

</group>

Domain Prohibit Status:


 -------------------------------------------------------------------------------
 The Registry contains ONLY .com.hk, .net.hk, .edu.hk, .org.hk,
 .gov.hk, idv.hk. and .hk $domains.
 -------------------------------------------------------------------------------

{{ ignore }}HOIS Terms of Use
</group>
By using this WHOIS search enquiry service you agree to these terms of use.
The data in HKDNR's WHOIS search engine is for informational purposes only and HKDNR does not guarantee the accuracy of the data. The data is provided to assist people obtaining information about the registration record of domain names registered by HKDNR. You agree to use the data for lawful purposes only.

In light of the General Data Protection Regulation, HKIRC reserves the right to not make available certain data on this WHOIS search enquiry.

You are not authorised to use high-volume, electronic or automated processes to access, query or harvest data from this WHOIS search enquiry service.

You agree that you will not and will not allow anyone else to:

a.    use the data for mass unsolicited commercial advertising of any sort via any media including telephone, email or fax; or

b.    enable high volume, automated or electronic processes that apply to HKDNR or its computer systems including the WHOIS search enquiry service; or

c.    without the prior written consent of HKDNR compile, repackage, disseminate, disclose to any third party or use the data for a purpose other than obtaining information about a domain name registration record; or

d.    use such data to derive an economic benefit for yourself.

HKIRC in its sole discretion may terminate your access to the WHOIS search enquiry service (including but not limited to blocking your IP address) at any time due to, including but not limited to, excessive use of the WHOIS search enquiry service.

HKDNR may modify these terms of use at any time by publishing the modified terms of use on its website.


<output macro="unpack" />
