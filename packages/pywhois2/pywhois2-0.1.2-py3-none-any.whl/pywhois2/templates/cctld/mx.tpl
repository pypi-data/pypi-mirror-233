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
    data = organization2parent('administrative contact', 'admin', data)
    data = organization2parent('technical contact', 'tech', data)
    data = organization2parent('billing contact', 'billing', data)
    data = name_servers2parent(data)
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
    if 'created' in data:
        if type(data['created']) == str:
            data['created'] = datetime.datetime.strptime(
                data['created'].replace('+0:00', '+00:00'),
                '%Y-%m-%d'
            ).replace(tzinfo=pytz.timezone(country_timezones['mx'][0]))

    # 有効期限
    if 'expiration' in data:
        if type(data['expiration']) == str:
            data['expiration'] = datetime.datetime.strptime(
                data['expiration'].replace('+0:00', '+00:00'),
                '%Y-%m-%d'
            ).replace(tzinfo=pytz.timezone(country_timezones['mx'][0]))

    # 最終更新
    if 'updated' in data:
        if type(data['updated']) == str:
            data['updated'] = datetime.datetime.strptime(
                data['updated'].replace('+0:00', '+00:00'),
                '%Y-%m-%d'
            ).replace(tzinfo=pytz.timezone(country_timezones['mx'][0]))

    return data

</macro>

## Template
## =======================================================

<group>
Domain Name:       {{ domain_name }}

Created On:        {{ created | ORPHRASE }}
Expiration Date:   {{ expiration | ORPHRASE }}
Last Updated On:   {{ updated | ORPHRASE }}
Registrar:         {{ registrar_name | ORPHRASE }}
URL:               {{ registrar_url | ORPHRASE }}
Whois TCP URI:     {{ registrar_whois_uri | ORPHRASE }}
Whois Web URL:     {{ registrar_whois_url | ORPHRASE }}

<group name="{{ group_type }}">
{{ group_type | ORPHRASE | lower }}:
   Name:           {{ name | ORPHRASE }}
   City:           {{ address | ORPHRASE | joinmatches(', ') }}
   State:          {{ address | ORPHRASE | joinmatches(', ') }}
   Country:        {{ country | ORPHRASE }}
</group>

<group name="name_servers">
Name Servers:{{ _start_ }}
   DNS:            {{ name_servers | lower | ORPHRASE | to_list | joinmatches }}
{{ _end_ }}
</group>

DNSSEC DS Records:
</group>

% NOTICE: The expiration date displayed in this record is the date the
% registrar's sponsorship of the domain name registration in the registry is
% currently set to expire. This date does not necessarily reflect the
% expiration date of the domain name registrant's agreement with the sponsoring
% registrar. Users may consult the sponsoring registrar's Whois database to
% view the registrar's reported date of expiration for this registration.

% The requested information ("Information") is provided only for the delegation
% of domain names and the operation of the DNS administered by NIC Mexico.

% It is absolutely prohibited to use the Information for other purposes,
% including sending not requested emails for advertising or promoting products
% and services purposes (SPAM) without the authorization of the owners of the
% Information and NIC Mexico.

% The database generated from the delegation system is protected by the
% intellectual property laws and all international treaties on the matter.

% If you need more information on the records displayed here, please contact us
% by email at ayuda@nic.mx .

% If you want notify the receipt of SPAM or unauthorized access, please send a
% email to abuse@nic.mx .

% NOTA: La fecha de expiracion mostrada en esta consulta es la fecha que el
% registrar tiene contratada para el nombre de dominio en el registry. Esta
% fecha no necesariamente refleja la fecha de expiracion del nombre de dominio
% que el registrante tiene contratada con el registrar. Puede consultar la base
% de datos de Whois del registrar para ver la fecha de expiracion reportada por
% el registrar para este nombre de dominio.

% La informacion que ha solicitado se provee exclusivamente para fines
% relacionados con la delegacion de nombres de dominio y la operacion del DNS
% administrado por NIC Mexico.

% Queda absolutamente prohibido su uso para otros propositos, incluyendo el
% envio de Correos Electronicos no solicitados con fines publicitarios o de
% promocion de productos y servicios (SPAM) sin mediar la autorizacion de los
% afectados y de NIC Mexico.

% La base de datos generada a partir del sistema de delegacion, esta protegida
% por las leyes de Propiedad Intelectual y todos los tratados internacionales
% sobre la materia.

% Si necesita mayor informacion sobre los registros aqui mostrados, favor de
% comunicarse a ayuda@nic.mx.

% Si desea notificar sobre correo no solicitado o accesos no autorizados, favor
% de enviar su mensaje a abuse@nic.mx.


<output macro="unpack" />
