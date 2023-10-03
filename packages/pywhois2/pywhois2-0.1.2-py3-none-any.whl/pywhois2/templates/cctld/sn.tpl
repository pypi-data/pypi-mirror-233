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

    data = status2parent(data)
    data = organization2parent('HOLDER', 'registrant', data)
    data = organization2parent('ADMIN_C', 'admin', data)
    data = organization2parent('TECH_C', 'tech', data)
    data = organization2parent('BILLING_C', 'billing', data)
    data = str2datetime(data)

    return data

def status2parent(data):
    from stringcase import pascalcase, snakecase
    if 'status' in data:
        extract_data = data['status']
        if type(extract_data) == str:
            del data['status']
            data['status'] = {}
            for line in extract_data.split(","):
                data['status'][line.lstrip().lower().replace('actif', 'active')] = True
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

    if 'created' in data:
        if type(data['created']) == str:
            data['created'] = datetime.datetime.fromisoformat(data['created'])

    if 'updated' in data:
        if type(data['updated']) == str:
            data['updated'] = datetime.datetime.fromisoformat(data['updated'])

    if 'expiration' in data:
        if type(data['expiration']) == str:
            data['expiration'] = datetime.datetime.fromisoformat(data['expiration'])

    return data
</macro>


## Template
## =======================================================

============================================================================
Whois du Registre .SN
Les informations fournies par ce service ne sont qu'à titre informatif.

Les données collectées via le formulaire d'enregistrement sont traitées exclusivement à des fins liées au traitement des domaines conformément à la RFC 3912 par le NIC Sénégal.

En application des dispositions de la loi n°2008-12 du 25 janvier 2008 portant sur la protection des données à caractère personnel, vous pouvez exercer vos droits d'accès, d'opposition, de rectification et de suppression auprès du NIC Sénégal - abuse(at)nic.sn.
============================================================================

<group>
Domain ID:                     {{ domain_id }}
Nom de domaine:                {{ domain_name }}
Date de création:              {{ created }}
Dernière modification:         {{ updated }}
Date d'expiration:             {{ expiration }}
Registrar:                     {{ registrar_name | ORPHRASE }}
Statut:                        {{ status }}

<group name="{{ type }}">
[{{ type }}]
ID Contact:                    {{ id }}
Type:                          {{ organization_type }}
Nom:                           {{ name | ORPHRASE }}
Adresse:                       {{ address | ORPHRASE | joinmatches(", ") }}
Code postal:                   {{ zip_code | ORPHRASE }}
Ville:                         {{ address | ORPHRASE | joinmatches(", ") }}
Pays:                          {{ country }}
Téléphone:                     {{ phone }}
Fax:                           {{ fax }}
Courriel:                      {{ email }}
Dernière modification:         {{ updated }}
</group>

Serveur de noms:               {{ name_servers | lower | ORPHRASE | to_list | joinmatches }}

DNSSEC:                        {{ dnssec }}
</group>

<output macro="unpack" />
