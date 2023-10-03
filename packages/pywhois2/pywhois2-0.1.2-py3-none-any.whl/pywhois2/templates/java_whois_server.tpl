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
    data = organization2parent('holder', 'registrant', data)
    data = organization2parent('admin_c', 'admin', data)
    data = organization2parent('tech_c', 'tech', data)
    data = organization2parent('registrar', 'registrar', data)

    if 'zone_c' in data:
        del data['zone_c']

    data = str2datetime(data)

    return data

def organization2parent(organization_type , organization_type_name, data):
    if organization_type in data:
        if type(data[organization_type]) == dict:
            extract_data = data[organization_type]
            del data[organization_type]

            for d in extract_data:
                data["{0}_{1}".format(organization_type_name,d)] = extract_data[d]
    return data

def str2datetime(data):
    import datetime
    import pytz
    from pytz import country_timezones

    if 'domain_name' in data:
        country_id = data['domain_name'].split('.')[-1]

        if 'created' in data:
            format = '%Y-%m-%d %H:%M:%S.0'
            if not len(data['created']) >= 12:
                format = '%Y-%m-%d'
            data['created'] = datetime.datetime.strptime(
                data['created'],
                format
            ).replace(tzinfo=pytz.timezone(country_timezones[country_id][0]))

        if 'updated' in data:
            format = '%Y-%m-%d %H:%M:%S.0'
            if not len(data['updated']) >= 12:
                format = '%Y-%m-%d'
            data['updated'] = datetime.datetime.strptime(
                data['updated'],
                format
            ).replace(tzinfo=pytz.timezone(country_timezones[country_id][0]))

        if 'expiration' in data:
            format = '%Y-%m-%d %H:%M:%S.0'
            if not len(data['expiration']) >= 12:
                format = '%Y-%m-%d'
            data['expiration'] = datetime.datetime.strptime(
                data['expiration'],
                format
            ).replace(tzinfo=pytz.timezone(country_timezones[country_id][0]))

        if 'registrant_created' in data:
            format = '%Y-%m-%d %H:%M:%S.0'
            if not len(data['registrant_created']) >= 12:
                format = '%Y-%m-%d'
            data['registrant_created'] = datetime.datetime.strptime(
                data['registrant_created'],
                format
            ).replace(tzinfo=pytz.timezone(country_timezones[country_id][0]))

        if 'registrant_updated' in data:
            format = '%Y-%m-%d %H:%M:%S.0'
            if not len(data['registrant_updated']) >= 12:
                format = '%Y-%m-%d'
            data['registrant_updated'] = datetime.datetime.strptime(
                data['registrant_updated'],
                format
            ).replace(tzinfo=pytz.timezone(country_timezones[country_id][0]))

        if 'registrant_expiration' in data:
            format = '%Y-%m-%d %H:%M:%S.0'
            if not len(data['registrant_expiration']) >= 12:
                format = '%Y-%m-%d'
            data['registrant_expiration'] = datetime.datetime.strptime(
                data['registrant_expiration'],
                format
            ).replace(tzinfo=pytz.timezone(country_timezones[country_id][0]))

        if 'admin_created' in data:
            format = '%Y-%m-%d %H:%M:%S.0'
            if not len(data['admin_created']) >= 12:
                format = '%Y-%m-%d'
            data['admin_created'] = datetime.datetime.strptime(
                data['admin_created'],
                format
            ).replace(tzinfo=pytz.timezone(country_timezones[country_id][0]))

        if 'admin_updated' in data:
            format = '%Y-%m-%d %H:%M:%S.0'
            if not len(data['admin_updated']) >= 12:
                format = '%Y-%m-%d'
            data['admin_updated'] = datetime.datetime.strptime(
                data['admin_updated'],
                format
            ).replace(tzinfo=pytz.timezone(country_timezones[country_id][0]))

        if 'admin_expiration' in data:
            format = '%Y-%m-%d %H:%M:%S.0'
            if not len(data['admin_expiration']) >= 12:
                format = '%Y-%m-%d'
            data['admin_expiration'] = datetime.datetime.strptime(
                data['admin_expiration'],
                format
            ).replace(tzinfo=pytz.timezone(country_timezones[country_id][0]))

        if 'tech_created' in data:
            format = '%Y-%m-%d %H:%M:%S.0'
            if not len(data['tech_created']) >= 12:
                format = '%Y-%m-%d'
            data['tech_created'] = datetime.datetime.strptime(
                data['tech_created'],
                format
            ).replace(tzinfo=pytz.timezone(country_timezones[country_id][0]))

        if 'tech_updated' in data:
            format = '%Y-%m-%d %H:%M:%S.0'
            if not len(data['tech_updated']) >= 12:
                format = '%Y-%m-%d'
            data['tech_updated'] = datetime.datetime.strptime(
                data['tech_updated'],
                format
            ).replace(tzinfo=pytz.timezone(country_timezones[country_id][0]))

        if 'tech_expiration' in data:
            format = '%Y-%m-%d %H:%M:%S.0'
            if not len(data['tech_expiration']) >= 12:
                format = '%Y-%m-%d'
            data['tech_expiration'] = datetime.datetime.strptime(
                data['tech_expiration'],
                format
            ).replace(tzinfo=pytz.timezone(country_timezones[country_id][0]))

    return data

</macro>


## Template
## =======================================================

This is JWhoisServer serving ccTLD tld;mq;gf;gp
Java Whois Server 0.4.1.3    (c) 2006 - 2015 Klaus Zerwes zero-sys.net
#########################################################################
# All data copyright of the organization unit running this server!
# By querying this server, you agree that you :
#	-may use this data only for lawful purposes;
#	-will not re-use data for any kind of support
#	  for the transmission of unsolicited advertising
#	  via e-mail, telephone, or facsimile;
#	-will not reproduce and/or store any part of the data
#	  without prior permission of the copyright holders;
#	-are aware of and agree to the fact that all access to the
#	  server is under constant monitoring and will be logged
#	  for the purpose of prosecution in case of missuse!
#########################################################################

<group del="_ignore_">
domain:     {{ domain_name }}
mntnr:      {{ _ignore_ }}
changed:    {{ updated | ORPHRASE }}
nameserver: {{ name_servers | lower | ORPHRASE | to_list | joinmatches }}

<group name="{{ group_type }}" del="_ignore_">
[{{ group_type }}]
mntnr:      {{ _ignore_ }}
type:       {{ type }}
name:       {{ name | ORPHRASE }}
address:    {{ address | ORPHRASE }}
pcode:      {{ zip_code }}
country:    {{ country }}
phone:      {{ phone }}
fax:        {{ fax }}
email:      {{ email }}
changed:    {{ updated | ORPHRASE }}
</group>
</group>

<output macro="unpack" />
