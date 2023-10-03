## Copyright (c) 2023 Blacknon. All rights reserved.
## Use of this source code is governed by an MIT license
## that can be found in the LICENSE file.
## =======================================================

## Macro
## =======================================================

<macro>
def standardize_status(data):
    if 'status' in data:
        if type(data['status']) == str:
            expiration = ' '.join(data['status'].split(" ")[:-1])
            del data['status']

            data['status'] = {
                "ok": False,
                "registered": False,
                "connected": False,
                "user_reserved": False,
                "advance_registered": False,
                "renamed": False,
                "to_be_deleted": False,
                "deleted": False,
                "negotiated": False,
            }

            if expiration == 'Registered':
                data['status']['ok'] = True
                data['status']['registered'] = True
            elif expiration == 'Connected':
                data['status']['ok'] = True
                data['status']['connected'] = True
            elif expiration == 'User-Reserved':
                data['status']['user_reserved'] = True
            elif expiration == 'Advance-Registered':
                data['status']['advance_registered'] = True
            elif expiration == 'Renamed':
                data['status']['renamed'] = True
            elif expiration == 'To be deleted':
                data['status']['to_be_deleted'] = True
            elif expiration == 'Deleted':
                data['status']['deleted'] = True
            elif expiration == 'Negotiated':
                data['status']['negotiated'] = True

    return data

def contact_address2parent(data):
    if 'contact_address' in data:
        extract_data = data['contact_address']
        del data['contact_address']
        for d in extract_data:
            for k in d.keys():
                data[k] = d[k]
    return data

def registrant_address2parent(data):
    if 'registrant_address' in data:
        extract_data = data['registrant_address']
        del data['registrant_address']
        for d in extract_data:
            for k in d.keys():
                data[k] = d[k]
    return data

def str2datetime(data):
    import datetime

    # 登録年月日
    if 'created' in data:
        if type(data['created']) == str:
            data['created'] = datetime.datetime.strptime(
                "{0} {1}".format(data['created'], "+0900"),
                '%Y/%m/%d %z'
            )

    # 有効期限
    if 'expiration' in data:
        if type(data['expiration']) == str:
            data['expiration'] = datetime.datetime.strptime(
                "{0} {1}".format(data['expiration'], "+0900"),
                '%Y/%m/%d %z'
            )

    # 最終更新
    if 'updated' in data:
        if type(data['updated']) == str:
            data['updated'] = datetime.datetime.strptime(
                data['updated'].replace("JST", "+0900"),
                '%Y/%m/%d %H:%M:%S (%z)'
            )

    return data
</macro>


## Template
## =======================================================

[ JPRS database provides information on network administration. Its use is    ]
[ restricted to network administration purposes. For further information,     ]
[ use 'whois -h whois.jprs.jp help'. To suppress Japanese output, add'/e'     ]
[ at the end of command, e.g. 'whois -h whois.jprs.jp xxx/e'.                 ]

<group macro="standardize_status, contact_address2parent, registrant_address2parent, str2datetime">
Domain Information: [ドメイン情報]
a. [ドメイン名]                   {{ domain_name | lower }}
b. [ねっとわーくさーびすめい]         {{ registrant_organization_local2 | ORPHRASE }}
c. [ネットワークサービス名]          {{ registrant_organization_local | ORPHRASE }}
d. [Network Service Name]       {{ registrant_organization | ORPHRASE }}
e. [そしきめい]                    {{ registrant_organization_local2 | ORPHRASE }}
f. [組織名]	                      {{ registrant_organization_local | ORPHRASE }}
g. [Organization]               {{ registrant_organization | ORPHRASE }}
h. [郵便番号]                     {{ registrant_zip_code }}
<group name="registrant_address">
i. [住所]                        {{ registrant_address_local | ORPHRASE  | joinmatches(" ") }}
                                {{ registrant_address_local | strip(' ') | ORPHRASE  | joinmatches(" ") }}
</group>
<group name="registrant_address">
j. [Address]                    {{ registrant_address | ORPHRASE  | joinmatches(", ") }}
                                {{ registrant_address | ORPHRASE  | joinmatches(", ") }}
</group>
k. [組織種別]                     {{ registrant_organization_type_local | ORPHRASE }}
l. [Organization Type]          {{ registrant_organization_type | ORPHRASE }}
m. [登録担当者]                    {{ registrant_name }}
n. [技術連絡担当者]                 {{ tech_name }}
o. [サービス提供者名]               {{ admin_name }}
p. [ネームサーバ]                  {{ name_servers | ORPHRASE | to_list | joinmatches }}
t. [代表法人名]                    {{ registrant_representative_corporation | ORPHRASE }}
w. [代表者名]                     {{ registrant_representative | ORPHRASE }}
u. [副代表法人名]                  {{ registrant_deputy_representative_corporation | ORPHRASE }}
x. [副代表者名]                    {{ registrant_deputy_representative | ORPHRASE }}
y. [通知アドレス]                  {{ registrant_email }}
[登録年月日]                      {{ created | ORPHRASE }}
[有効期限]                        {{ expiration | ORPHRASE }}
[状態]                           {{ status | ORPHRASE }}
[最終更新]                        {{ updated | ORPHRASE }}

Contact Information: [公開連絡窓口]
[名前]                           {{ contact_name_local | ORPHRASE }}
[Name]                          {{ contact_name | ORPHRASE }}
[Email]                         {{ contact_email | ORPHRASE }}
[Web Page]                      {{ contact_web_page | ORPHRASE }}
[郵便番号]                        {{ contact_zip_code | ORPHRASE }}
<group name="contact_address">
[住所]                           {{ contact_address_local | ORPHRASE | joinmatches(" ") }}
                                {{ contact_address_local | strip(' ') | ORPHRASE  | joinmatches(" ") }}
</group>
<group name="contact_address">
[Postal Address]                {{ contact_address | ORPHRASE | joinmatches(", ") }}
                                {{ contact_address | strip(' ') | ORPHRASE  | joinmatches(", ") }}
</group>
[電話番号]                        {{ contact_phone | ORPHRASE }}
[FAX番号]                        {{ contact_fax | ORPHRASE }}
</group>
