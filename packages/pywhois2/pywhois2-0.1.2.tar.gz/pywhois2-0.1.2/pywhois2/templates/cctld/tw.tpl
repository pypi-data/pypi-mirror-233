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
        '   Registrant:',
        '   Administrative Contact:',
        '   Technical Contact:',
    ]

    before_line = ''
    for line in data.splitlines():
        if line in group_header_line:
            new_data.append('')

        if not before_line in group_header_line:
            new_data.append(line)
        else:
            if line != '      ':
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

    data = name_servers2parent(data)
    data = registrant_parse(data)
    data = admin_parse(data)
    data = tech_parse(data)
    data = standardize_status(data)
    data = str2datetime(data)

    return data

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
    if 'registrant' in data:
        extract_data = data['registrant']
        del data['registrant']
        data['registrant_name'] = extract_data['line'][0]
        data['registrant_email'] = extract_data['line'][1]
        data['registrant_country'] = extract_data['line'][2]
    return data

def admin_parse(data):
    if 'admin' in data:
        extract_data = data['admin']
        del data['admin']

        if len(extract_data['line']) > 1:
            data['admin_name'] = extract_data['line'][1]
    return data

def tech_parse(data):
    if 'tech' in data:
        extract_data = data['tech']
        del data['tech']

        if len(extract_data['line']) > 1:
            data['tech_name'] = extract_data['line'][1]
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
                data['created'].replace("UTC+8", "+08:00"),
                '%Y-%m-%d %H:%M:%S (%z)'
            ).replace(tzinfo=pytz.timezone(country_timezones['tw'][0]))

    # 有効期限
    if 'expiration' in data:
        if type(data['expiration']) == str:
            data['expiration'] = datetime.datetime.strptime(
                data['expiration'].replace("UTC+8", "+08:00"),
                '%Y-%m-%d %H:%M:%S (%z)'
            ).replace(tzinfo=pytz.timezone(country_timezones['tw'][0]))

    # 最終更新
    if 'updated' in data:
        if type(data['updated']) == str:
            data['updated'] = datetime.datetime.strptime(
                data['updated'].replace("UTC+8", "+08:00"),
                '%Y-%m-%d %H:%M:%S (%z)'
            ).replace(tzinfo=pytz.timezone(country_timezones['tw'][0]))

    return data
</macro>




## Template
## =======================================================

<input macro="delete_empty_line" />

<group>
Domain Name: {{ domain_name | ORPHRASE }}
   Domain Status: {{ status | ORPHRASE }}

<group name="registrant">
   Registrant:{{ _start_ }}
      {{ line | _line_ | to_list | joinmatches }}
{{ _end_ }}
</group>

<group name="admin">
   Administrative Contact:{{ _start_ }}
      {{ line | _line_ | to_list | joinmatches }}
{{ _end_ }}
</group>

<group name="tech">
   Technical Contact:{{ _start_ }}
      {{ line | _line_ | to_list | joinmatches }}
{{ _end_ }}
</group>

   Record expires on {{ expiration | ORPHRASE }}
   Record created on {{ created | ORPHRASE }}

<group name="name_servers">
   Domain servers in listed order:{{ _start_ }}
      {{ name_servers | lower | to_list | joinmatches }}
{{ _end_ }}
</group>

Registration Service Provider: {{ registrar_name | ORPHRASE }}
Registration Service URL: {{ registrar_url | ORPHRASE }}

Provided by Registry Services, LLC. Registry Gateway Services

%%% end %%% {{ ignore }} %%% end %%%
</group>


<output macro="unpack" />
