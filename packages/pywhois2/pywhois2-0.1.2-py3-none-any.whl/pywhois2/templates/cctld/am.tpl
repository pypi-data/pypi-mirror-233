## Copyright (c) 2023 Blacknon. All rights reserved.
## Use of this source code is governed by an MIT license
## that can be found in the LICENSE file.
## =======================================================

## 何故かgroupの削除が行われないので要調査(とりあえず、しばらくはこのままでいいか…)

## Macro
## =======================================================

<macro>
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

def registrant_parse(data):
    if 'registrant_name' in data:
        extract_data = data['registrant_name']
        del data['registrant_name']
        data['registrant_name'] = extract_data['line'][0]
        data['registrant_address'] = extract_data['line'][1]
        data['registrant_address'] += ",".join(extract_data['line'][2].split(",")[:-1])
        data['registrant_zip_code'] = extract_data['line'][2].split(",")[-1].lstrip()
        data['registrant_country'] = extract_data['line'][3]
    return data

def admin_parse(data):
    if 'admin_name' in data:
        extract_data = data['admin_name']
        del data['admin_name']
        data['admin_name'] = extract_data['line'][0]
        data['admin_organization'] = extract_data['line'][1]
        data['admin_address'] = extract_data['line'][2]
        data['admin_address'] += extract_data['line'][3]
        data['admin_country'] = extract_data['line'][4]
        data['admin_email'] = extract_data['line'][5]
        data['admin_phone'] = extract_data['line'][6]
        data['admin_fax'] = extract_data['line'][7]
    return data

def tech_parse(data):
    if 'tech_name' in data:
        extract_data = data['tech_name']
        del data['tech_name']
        data['tech_name'] = extract_data['line'][0]
        data['tech_organization'] = extract_data['line'][1]
        data['tech_address'] = extract_data['line'][2]
        data['tech_address'] += extract_data['line'][3]
        data['tech_country'] = extract_data['line'][4]
        data['tech_email'] = extract_data['line'][5]
        data['tech_phone'] = extract_data['line'][6]
        data['tech_fax'] = extract_data['line'][7]
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
                data['created'],
                '%Y-%m-%d'
            ).replace(tzinfo=pytz.timezone(country_timezones['am'][0]))

    # 有効期限
    if 'expiration' in data:
        if type(data['expiration']) == str:
            data['expiration'] = datetime.datetime.strptime(
                data['expiration'],
                '%Y-%m-%d'
            ).replace(tzinfo=pytz.timezone(country_timezones['am'][0]))

    # 最終更新
    if 'updated' in data:
        if type(data['updated']) == str:
            data['updated'] = datetime.datetime.strptime(
                data['updated'],
                '%Y-%m-%d'
            ).replace(tzinfo=pytz.timezone(country_timezones['am'][0]))

    return data
</macro>

## Template
## =======================================================

<group macro="standardize_status, registrant_parse, admin_parse, tech_parse, name_servers2parent, str2datetime" >
   Domain name: {{ domain_name | lower | ORPHRASE }}
   Registrar:   {{ registrar_id }} ({{ registrar_name | ORPHRASE }})
   Status:      {{ status | lower | ORPHRASE }}

<group name="registrant_name">
   Registrant:{{ _start_ }}
      {{ line | _line_ | to_list | joinmatches }}
{{ _end_ }}
</group>

<group name="admin_name">
   Administrative contact:{{ _start_ }}
      {{ line | _line_ | to_list | joinmatches }}
{{ _end_ }}
</group>

<group name="tech_name">
   Technical contact:{{ _start_ }}
      {{ line | _line_ | to_list | joinmatches }}
{{ _end_ }}
</group>

<group name="name_servers">
   DNS servers:{{ _start_ }}
      {{ name_servers | strip(' ') | ORPHRASE | to_list | joinmatches }}
{{ _end_ }}
</group>

<group name="name_servers">
   DNS servers{{ strip(' ') | ORPHRASE }}:{{ _start_ }}
      {{ name_servers | strip(' ') | ORPHRASE | to_list | joinmatches }}
{{ _end_ }}
</group>

   Registered:    {{ created | ORPHRASE }}
   Last modified: {{ updated | ORPHRASE }}
   Expires:       {{ expiration | ORPHRASE }}
</group>
