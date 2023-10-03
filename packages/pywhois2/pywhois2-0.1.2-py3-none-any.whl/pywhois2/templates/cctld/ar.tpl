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
            format = '%Y-%m-%d %H:%M:%S'
            if len(data['created']) > 19:
                format = '%Y-%m-%d %H:%M:%S.%f'

            data['created'] = datetime.datetime.strptime(
                data['created'],
                format
            ).replace(tzinfo=pytz.timezone(country_timezones['ar'][0]))

    # 最終更新
    if 'updated' in data:
        if type(data['updated']) == str:
            format = '%Y-%m-%d %H:%M:%S'
            if len(data['updated']) > 19:
                format = '%Y-%m-%d %H:%M:%S.%f'

            data['updated'] = datetime.datetime.strptime(
                data['updated'],
                format
            ).replace(tzinfo=pytz.timezone(country_timezones['ar'][0]))

    # 有効期限
    if 'expiration' in data:
        if type(data['expiration']) == str:
            format = '%Y-%m-%d %H:%M:%S'
            if len(data['expiration']) > 19:
                format = '%Y-%m-%d %H:%M:%S.%f'

            data['expiration'] = datetime.datetime.strptime(
                data['expiration'],
                format
            ).replace(tzinfo=pytz.timezone(country_timezones['ar'][0]))

    if 'contact_creation' in data:
        if type(data['contact_creation']) == str:
            format = '%Y-%m-%d %H:%M:%S'
            if len(data['contact_creation']) > 19:
                format = '%Y-%m-%d %H:%M:%S.%f'

            data['contact_creation'] = datetime.datetime.strptime(
                data['contact_creation'],
                format
            ).replace(tzinfo=pytz.timezone(country_timezones['ar'][0]))

    return data
</macro>

## Template
## =======================================================

% La información a la que estás accediendo se provee exclusivamente para
% fines relacionados con operaciones sobre nombres de dominios y DNS,
% quedando absolutamente prohibido su uso para otros fines.
%
% La DIRECCIÓN NACIONAL DEL REGISTRO DE DOMINIOS DE INTERNET es depositaria
% de la información que los usuarios declaran con la sola finalidad de
% registrar nombres de dominio en ‘.ar’, para ser publicada en el sitio web
% de NIC Argentina.
%
% La información personal que consta en la base de datos generada a partir
% del sistema de registro de nombres de dominios se encuentra amparada por
% la Ley N° 25326 “Protección de Datos Personales” y el Decreto
% Reglamentario 1558/01.

<group macro="str2datetime">
domain:		{{ domain_name }}
registrant:	{{ registrant_id | ORPHRASE }}
registrar:	{{ registrar_name | ORPHRASE }}
registered:	{{ created | ORPHRASE }}
changed:	{{ updated | ORPHRASE }}
expire:		{{ expiration | ORPHRASE }}

contact:	{{ contact_id | ORPHRASE }}
name:		{{ contact_name | ORPHRASE }}
registrar:	{{ registrar_name | ORPHRASE }}
created:	{{ contact_created | ORPHRASE }}
changed:	{{ contact_updated | ORPHRASE }}

nserver:	{{ name_servers | ORPHRASE | to_list | joinmatches }}
registrar:	{{ registrar_name | ORPHRASE }}
created:	{{ name_servers_created | ORPHRASE }}
</group>
