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
            update_d = {}
            for dd in data[d]:
                if type(dd) == dict:
                    update_d.update(dd)
                    update_data[d] = update_d
                else:
                    if d not in update_data:
                        update_data[d] = list()
                    update_data[d].append(dd)
        else:
            update_data[d] = data[d]
    data = update_data

    data = standardize_status(data)
    data = lookup(data)
    data = str2datetime(data)
    data = name_servers2parent(data)
    data = cleanup(data)

    return data

def cleanup(data):
    update_data = {}

    for d in data:
        if type(data[d]) == dict:
            if 'registrar_id' not in data[d]:
                update_data[d] = data[d]
        else:
            update_data[d] = data[d]

    data = update_data
    return data


def standardize_status(data):
    from stringcase import pascalcase, snakecase
    if 'status' in data:
        if type(data['status']) == list:
            extract_data = data['status']
            del data['status']
            data['status'] = {}

            for d in extract_data:
                data['status'][snakecase(d.lstrip())] = True

    return data

def lookup(data):
    registrant_id = ''
    admin_id = ''
    tech_id = ''

    if 'registrant_id' in data:
        registrant_id = data['registrant_id']
        if registrant_id in data:
            extract_data = data[registrant_id]
            del data['registrant_id']

            for d in extract_data:
                data['registrant_{0}'.format(d)] = extract_data[d]

    if 'admin_id' in data:
        admin_id = data['admin_id']
        if admin_id in data:
            extract_data = data[data['admin_id']]
            del data['admin_id']

            for d in extract_data:
                data['admin_{0}'.format(d)] = extract_data[d]

    if 'tech_id' in data:
        tech_id = data['tech_id']
        if tech_id in data:
            extract_data = data[tech_id]
            del data['tech_id']

            for d in extract_data:
                data['tech_{0}'.format(d)] = extract_data[d]

    if registrant_id != '':
        if registrant_id in data:
            del data[registrant_id]

    if admin_id != '':
        if admin_id in data:
            del data[admin_id]

    if tech_id != '':
        if tech_id in data:
            del data[tech_id]

    return data

def str2datetime(data):
    import datetime
    import pytz
    from pytz import country_timezones

    if 'domain_name' in data:
        country_id = data['domain_name'].split('.')[-1]

        if 'created' in data:
            format = '%d.%m.%Y %H:%M:%S'
            if not len(data['created']) >= 12:
                format = '%d.%m.%Y'
            data['created'] = datetime.datetime.strptime(
                data['created'],
                format
            ).replace(tzinfo=pytz.timezone(country_timezones[country_id][0]))

        if 'updated' in data:
            format = '%d.%m.%Y %H:%M:%S'
            if not len(data['updated']) >= 12:
                format = '%d.%m.%Y'
            data['updated'] = datetime.datetime.strptime(
                data['updated'],
                format
            ).replace(tzinfo=pytz.timezone(country_timezones[country_id][0]))

        if 'expiration' in data:
            format = '%d.%m.%Y %H:%M:%S'
            if not len(data['expiration']) >= 12:
                format = '%d.%m.%Y'
            data['expiration'] = datetime.datetime.strptime(
                data['expiration'],
                format
            ).replace(tzinfo=pytz.timezone(country_timezones[country_id][0]))


        if 'registrant_created' in data:
            format = '%d.%m.%Y %H:%M:%S'
            if not len(data['registrant_created']) >= 12:
                format = '%d.%m.%Y'
            data['registrant_created'] = datetime.datetime.strptime(
                data['registrant_created'],
                format
            ).replace(tzinfo=pytz.timezone(country_timezones[country_id][0]))

        if 'registrant_updated' in data:
            format = '%d.%m.%Y %H:%M:%S'
            if not len(data['registrant_updated']) >= 12:
                format = '%d.%m.%Y'
            data['registrant_updated'] = datetime.datetime.strptime(
                data['registrant_updated'],
                format
            ).replace(tzinfo=pytz.timezone(country_timezones[country_id][0]))

        if 'registrant_expiration' in data:
            format = '%d.%m.%Y %H:%M:%S'
            if not len(data['registrant_expiration']) >= 12:
                format = '%d.%m.%Y'
            data['registrant_expiration'] = datetime.datetime.strptime(
                data['registrant_expiration'],
                format
            ).replace(tzinfo=pytz.timezone(country_timezones[country_id][0]))


        if 'admin_created' in data:
            format = '%d.%m.%Y %H:%M:%S'
            if not len(data['admin_created']) >= 12:
                format = '%d.%m.%Y'
            data['admin_created'] = datetime.datetime.strptime(
                data['admin_created'],
                format
            ).replace(tzinfo=pytz.timezone(country_timezones[country_id][0]))

        if 'admin_updated' in data:
            format = '%d.%m.%Y %H:%M:%S'
            if not len(data['admin_updated']) >= 12:
                format = '%d.%m.%Y'
            data['admin_updated'] = datetime.datetime.strptime(
                data['admin_updated'],
                format
            ).replace(tzinfo=pytz.timezone(country_timezones[country_id][0]))

        if 'admin_expiration' in data:
            format = '%d.%m.%Y %H:%M:%S'
            if not len(data['admin_expiration']) >= 12:
                format = '%d.%m.%Y'
            data['admin_expiration'] = datetime.datetime.strptime(
                data['admin_expiration'],
                format
            ).replace(tzinfo=pytz.timezone(country_timezones[country_id][0]))


        if 'tech_created' in data:
            format = '%d.%m.%Y %H:%M:%S'
            if not len(data['tech_created']) >= 12:
                format = '%d.%m.%Y'
            data['tech_created'] = datetime.datetime.strptime(
                data['tech_created'],
                format
            ).replace(tzinfo=pytz.timezone(country_timezones[country_id][0]))

        if 'tech_updated' in data:
            format = '%d.%m.%Y %H:%M:%S'
            if not len(data['tech_updated']) >= 12:
                format = '%d.%m.%Y'
            data['tech_updated'] = datetime.datetime.strptime(
                data['tech_updated'],
                format
            ).replace(tzinfo=pytz.timezone(country_timezones[country_id][0]))

        if 'tech_expiration' in data:
            format = '%d.%m.%Y %H:%M:%S'
            if not len(data['tech_expiration']) >= 12:
                format = '%d.%m.%Y'
            data['tech_expiration'] = datetime.datetime.strptime(
                data['tech_expiration'],
                format
            ).replace(tzinfo=pytz.timezone(country_timezones[country_id][0]))

    return data

def name_servers2parent(data):
    update_data = {}

    for d in data:
        if type(data[d]) == dict:
            if 'name_servers' in data[d]:
                extract_data = data[d]
                update_data['name_servers'] = extract_data['name_servers']
            else:
                update_data[d] = data[d]
        else:
            update_data[d] = data[d]

    data = update_data
    return data
</macro>



## Template
## =======================================================

%  *The information provided by WHOIS is supplied by NIC Costa Rica's database of registered domains. This option has the sole intention of showing information about the domains registered under the CR Top level domain for name assignation purposes. It is absolutely forbidden to collect, store, use or transmit any information displayed by WHOIS for commercial and advertising purposes without prior notice to the persons involved and to NIC Costa Rica. NIC Costa Rica does not guarantee the accuracy of the information displayed by this option. Since it is provided by the contacts, the accuracy is their responsibility. The National Academy of Sciences is not liable for the use of the information here revealed. The National Academy of Sciences undertakes to comply with the terms set forth in the Data Protection laws of the Republic of Costa Rica and therefore protects the data collected from NIC Costa Rica users, regardless of whether they are Costa Rican citizens or not. If you are a contact of a .cr domain name and wish to use the WHOIS Privacy service, select this option in "Edit account" once your login with your username and password, or access the following link:
% https://www.nic.cr/iniciar-sesion/?next=/my-account/
%
%
% *La información mostrada a través de la opción WHOIS es provista de la base de datos de los dominios registrados en NIC Costa Rica. Esta opción tiene el propósito exclusivo de mostrar información sobre los dominios registrados bajo el Dominio Superior .CR para los fines de la delegación de los nombs. Queda absolutamente prohibido compilar, almacenar, usar y/o trasmitir la información mostrada mediante la opción WHOIS para fines comerciales y publicitarios, sin la previa autorización de los afectados y de NIC Costa Rica. NIC Costa Rica no garantiza la exactitud de la información desplegada mediante esta opción, ya que ésta proviene de los contactos, y su veracidad es responsabilidad de estos últimos. La Academia Nacional de Ciencias no se responsabiliza por el uso que se le dé a la información aquí mostrada. La Academia Nacional de Ciencias se compromete a cumplir con los términos establecidos en las leyes de Protección de Datos de la República de Costa Rica y por lo tanto protege los datos recolectados de todos los usuarios de NIC Costa Rica que sean ciudadanos o no de la República de Costa Rica. Si un contacto de un dominio .cr desea hacer uso del servicio de Privacidad WHOIS puede escoger esta opción en "Editar cuenta" con su usuario y clave, o ingresar al siguiente link:
% https://www.nic.cr/iniciar-sesion/?next=/mi-cuenta/
%
% Whoisd Server Version: 3.12.2
% Timestamp: Sun Sep 17 21:02:26 2023

<group del="_ignore_">
domain:       {{ domain_name | lower | ORPHRASE }}
registrant:   {{ registrant_id }}
admin-c:      {{ admin_id }}
tech-c:       {{ tech_id }}
nsset:        {{ nsset_group_id }}
registrar:    {{ registrar_id }}
status:       {{ status | ORPHRASE | to_list | joinmatches }}
registered:   {{ created | ORPHRASE }}
changed:      {{ updated | ORPHRASE }}
expire:       {{ expiration | ORPHRASE }}

<group name="{{ contact_id }}">
contact:      {{ contact_id }}
org:          {{ organization | ORPHRASE }}
name:         {{ name | ORPHRASE }}
address:      {{ registrant_address | ORPHRASE | joinmatches(", ") }}
phone:        {{ phone | ORPHRASE }}
fax-no:       {{ fax | ORPHRASE }}
e-mail:       {{ email | ORPHRASE }}
registrar:    {{ registrar_id }}
created:      {{ created | ORPHRASE }}
changed:      {{ updated | ORPHRASE }}
{{ _end_ }}
</group>

<group name="{{ nsset_id }}">
nsset:        {{ nsset_id }}
nserver:      {{ name_servers | lower | ORPHRASE | to_list | joinmatches }}
tech-c:       {{ tech_id }}
registrar:    {{ registrar_id }}
created:      {{ created | ORPHRASE }}
changed:      {{ updated | ORPHRASE }}
{{ _end_ }}
</group>

%%% end %%% {{ _ignore_ }} %%% end %%%
</group>

<output macro="unpack" />
