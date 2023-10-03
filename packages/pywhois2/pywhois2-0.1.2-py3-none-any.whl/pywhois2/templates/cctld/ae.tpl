## Copyright (c) 2023 Blacknon. All rights reserved.
## Use of this source code is governed by an MIT license
## that can be found in the LICENSE file.
## =======================================================

## Macro
## =======================================================

<macro>
from stringcase import pascalcase, snakecase
def standardize_status(data):
    if 'status' in data:
        if type(data['status']) == list:
            extract_data = data['status']
            del data['status']
            data['status'] = {}

            for d in extract_data:
                data['status'][snakecase(d.lstrip())] = True

    return data

</macro>

## Template
## =======================================================

<group macro="standardize_status">
Domain Name:                     {{ domain_name }}
Registrar ID:                    {{ registrar_id | ORPHRASE }}
Registrar Name:                  {{ registrar_name | ORPHRASE }}
Status:                          {{ status | ORPHRASE | to_list | joinmatches }}

Registrant Contact ID:           {{ registrant_id | ORPHRASE }}
Registrant Contact Name:         {{ registrant_name | ORPHRASE }}
Registrant Contact Email:        {{ registrant_email | ORPHRASE }}
Registrant Contact Organisation: {{ registrant_organization | ORPHRASE }}

Tech Contact ID:                 {{ tech_id | ORPHRASE }}
Tech Contact Name:               {{ tech_name | ORPHRASE }}
Tech Contact Email:              {{ tech_email | ORPHRASE }}
Tech Contact Organisation:       {{ tech_organization | ORPHRASE }}

Name Server:                     {{ name_servers | ORPHRASE | to_list | joinmatches }}
</group>
