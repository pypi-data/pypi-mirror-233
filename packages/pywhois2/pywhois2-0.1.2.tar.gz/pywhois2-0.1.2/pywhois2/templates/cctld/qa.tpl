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
                data['status'][line.lstrip().lower()] = True
    return data

</macro>


## Template
## =======================================================

<group macro="status2parent">
Domain Name:                     {{ domain_name }}
Registrar ID:                    {{ registrar_id }}
Registrar Name:                  {{ registrar_name | ORPHRASE }}
Status:                          {{ status }}

Registrant:                      {{ registrant_name | ORPHRASE }}
Eligibility Type:                {{ eligibility_type | ORPHRASE }}
Eligibility ID:                  {{ eligibility_id | ORPHRASE }}

Name Server:                     {{ name_servers | lower | ORPHRASE | to_list | joinmatches }}
</group>
