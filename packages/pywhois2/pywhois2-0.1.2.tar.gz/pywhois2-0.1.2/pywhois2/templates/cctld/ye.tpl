## Copyright (c) 2023 Blacknon. All rights reserved.
## Use of this source code is governed by an MIT license
## that can be found in the LICENSE file.
## =======================================================

## Macro
## =======================================================

## Template
## =======================================================

<group>
Domain Name: {{ domain_name }}
Registrar Name: {{ registrar_name | ORPHRASE }}
Registrant Organization: {{registrant_organization | ORPHRASE }}
Name Server: {{ name_servers | lower | ORPHRASE | to_list | joinmatches }}
</group>
