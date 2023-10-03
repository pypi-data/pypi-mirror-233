[ JPRS database provides information on network administration. Its use is    ]
[ restricted to network administration purposes. For further information,     ]
[ use 'whois -h whois.jprs.jp help'. To suppress Japanese output, add'/e'     ]
[ at the end of command, e.g. 'whois -h whois.jprs.jp xxx/e'.                 ]

<group>
Domain Information: [ドメイン情報]
a. [ドメイン名]                   {{ domain_name | lower }}
b. [ねっとわーくさーびすめい]         {{ registrant_organization_local2 | _line_ | strip('\n') | strip('\r') }}
c. [ネットワークサービス名]          {{ registrant_organization_local | _line_ | strip('\n') | strip('\r') }}
d. [Network Service Name]       {{ registrant_organization | _line_ | strip('\n') | strip('\r') }}
e. [そしきめい]                    {{ registrant_organization_local2 | _line_ | strip('\n') | strip('\r') }}
f. [組織名]	                      {{ registrant_organization_local | _line_ | strip('\n') | strip('\r') }}
g. [Organization]               {{ registrant_organization | _line_ | strip('\n') | strip('\r') }}
h. [郵便番号]                     {{ registrant_zip_code }}
<group name="registrant_address">
i. [住所]                        {{ registrant_address_local | _line_ | strip('\n') | strip('\r')  | joinmatches(" ") }}
                                {{ registrant_address_local | strip(' ') | _line_ | strip('\n') | strip('\r')  | joinmatches(" ") }}
</group>
<group name="registrant_address">
j. [Address]                    {{ registrant_address | _line_ | strip('\n') | strip('\r')  | joinmatches(" ") }}
                                {{ registrant_address | _line_ | strip('\n') | strip('\r')  | joinmatches(" ") }}
</group>
k. [組織種別]                     {{ registrant_organization_type_local | _line_ | strip('\n') | strip('\r') }}
l. [Organization Type]          {{ registrant_organization_type | _line_ | strip('\n') | strip('\r') }}
m. [登録担当者]                    {{ registrant_name }}
n. [技術連絡担当者]                 {{ tech_name }}
o. [サービス提供者名]               {{ admin_name }}
p. [ネームサーバ]                  {{ name_servers | _line_ | strip('\n') | strip('\r') | to_list | joinmatches }}
t. [代表法人名]                    {{ registrant_representative_corporation | _line_ | strip('\n') | strip('\r') }}
w. [代表者名]                     {{ registrant_representative | _line_ | strip('\n') | strip('\r') }}
u. [副代表法人名]                  {{ registrant_deputy_representative_corporation | _line_ | strip('\n') | strip('\r') }}
x. [副代表者名]                    {{ registrant_deputy_representative | _line_ | strip('\n') | strip('\r') }}
y. [通知アドレス]                  {{ registrant_email }}
[登録年月日]                      {{ creation_date | _line_ | strip('\n') | strip('\r') }}
[有効期限]                        {{ expiration_date | _line_ | strip('\n') | strip('\r') }}
[状態]                           {{ status | _line_ | strip('\n') | strip('\r') }}
[最終更新]                        {{ last_updated | _line_ | strip('\n') | strip('\r') }}

Contact Information: [公開連絡窓口]
[名前]                           {{ contact_name_local | _line_ | strip('\n') | strip('\r') }}
[Name]                          {{ contact_name | _line_ | strip('\n') | strip('\r') }}
[Email]                         {{ contact_email | _line_ | strip('\n') | strip('\r') }}
[Web Page]                      {{ contact_web_page | _line_ | strip('\n') | strip('\r') }}
[郵便番号]                        {{ contact_zip_code | _line_ | strip('\n') | strip('\r') }}
<group name="contact_address">
[住所]                           {{ contact_address_local | _line_ | strip('\n') | strip('\r') | joinmatches(" ") }}
                                {{ contact_address_local | strip(' ') | _line_ | strip('\n') | strip('\r')  | joinmatches(" ") }}
</group>
<group name="contact_address">
[Postal Address]                {{ contact_address | _line_ | strip('\n') | strip('\r') | joinmatches(" ") }}
                                {{ contact_address | strip(' ') | _line_ | strip('\n') | strip('\r')  | joinmatches(" ") }}
</group>
[電話番号]                        {{ contact_phone | _line_ | strip('\n') | strip('\r') }}
[FAX番号]                        {{ contact_fax | _line_ | strip('\n') | strip('\r') }}
</group>
