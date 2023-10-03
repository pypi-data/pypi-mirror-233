pywhois2
===

python whois parser command and library, that use [template text parser(ttp)](https://github.com/dmulyalin/ttp).

## Feture

- Parsing is based on text templates, making it easy to add target domains.
- Local language information is also subject to management.

But, currently under development, the status is as follows.

- Time and time zone information may be in text format
- May contain unnecessary data

## Install

```bash
git clone https://github.com/blacknon/pywhois2
cd pywhois2
pip install ./
```

## Usage

### Command

```shell
$ whois2 myna.go.jp | jq
{
  "updated": "2023/02/01 01:11:56 +0900",
  "created": "2022/01/06 00:00:00 +0900",
  "tech_name": "KA35357JP",
  "registrant_name": "KA35357JP",
  "registrant_organization_type": "Government",
  "registrant_organization_type_local": "政府機関",
  "registrant_organization": "Accounting Division,Digital Agency",
  "registrant_organization_local": "デジタル庁 戦略・組織グループ会計担当",
  "registrant_organization_local2": "でじたるちょう せんりゃくそしきぐるーぷ かいけいたんとう",
  "domain_name": "myna.go.jp",
  "name_servers": [
    "ns-1048.awsdns-03.org",
    "ns-1605.awsdns-08.co.uk",
    "ns-680.awsdns-21.net",
    "ns-432.awsdns-54.com"
  ],
  "status": {
    "ok": true,
    "registered": false,
    "connected": true,
    "user_reserved": false,
    "advance_registered": false,
    "renamed": false,
    "to_be_deleted": false,
    "deleted": false,
    "negotiated": false
  }
}

$ whois2 google.co.kr | jq
{
  "publish_status": "Y",
  "expiration": "2024/07/28 00:00:00 +0828",
  "updated": "2010/10/04 00:00:00 +0828",
  "created": "1999/07/28 00:00:00 +0828",
  "admin_phone": "82.25319000",
  "admin_email": "dns-admin@google.com",
  "registrant_zip_code": "135984",
  "registrant_address": "22nd Floor Gangnam Finance Center 737, Yeoksam-dong Kangnam-ku Seoul",
  "registrant_name": "Google Korea, LLC",
  "domain_name": "google.co.kr",
  "registrant_address_local": "서울시 강남구 역삼동 737 강남파이낸스센터 22층",
  "registrant_name_local": "구글코리아유한회사",
  "dnssec": "unsigned",
  "name_servers": [
    "ns1.google.com",
    "ns2.google.com",
    "ns3.google.com",
    "ns4.google.com"
  ]
}

$ whois2 google.com | jq
{
  "dnssec": "unsigned",
  "tech_email": "Select Request Email Form at https://domains.markmonitor.com/whois/google.com",
  "tech_country": "US",
  "tech_organization": "Google LLC",
  "admin_email": "Select Request Email Form at https://domains.markmonitor.com/whois/google.com",
  "admin_country": "US",
  "admin_organization": "Google LLC",
  "registrant_email": "Select Request Email Form at https://domains.markmonitor.com/whois/google.com",
  "registrant_country": "US",
  "registrant_organization": "Google LLC",
  "registrar_phone": "+1.2086851750",
  "registrar_email": "abusecomplaints@markmonitor.com",
  "registrar_id": "292",
  "registrar_name": "MarkMonitor, Inc.",
  "expiration": "2028/09/13 07:00:00 +0000",
  "created": "1997/09/15 07:00:00 +0000",
  "updated": "2019/09/09 15:39:04 +0000",
  "registrar_whois_url": "http://www.markmonitor.com",
  "registrar_whois_server": "whois.markmonitor.com",
  "registry_domain_id": "2138514_domain_com-vrsn",
  "domain_name": "google.com",
  "registrant_address": "CA",
  "admin_address": "CA",
  "tech_address": "CA",
  "name_servers": [
    "ns1.google.com",
    "ns3.google.com",
    "ns4.google.com",
    "ns2.google.com"
  ],
  "status": {
    "auto_renew_period": false,
    "inactive": false,
    "ok": false,
    "pending_create": false,
    "pending_delete": false,
    "pending_renew": false,
    "pending_restore": false,
    "pending_transfer": false,
    "pending_update": false,
    "redemption_period": false,
    "renew_period": false,
    "server_delete_prohibited": true,
    "server_hold": false,
    "server_renew_prohibited": false,
    "server_transfer_prohibited": true,
    "server_update_prohibited": true,
    "transfer_period": false,
    "client_delete_prohibited": true,
    "client_hold": false,
    "client_renew_prohibited": false,
    "client_transfer_prohibited": true,
    "client_update_prohibited": true
  }
}
```

### Library

```python
from pywhois2 import Whois
import json
import datetime


def json_serial(obj):
    if isinstance(obj, (datetime.datetime, datetime.date)):
        return obj.strftime("%Y/%m/%d %H:%M:%S %z")
    # 上記以外はサポート対象外.
    raise TypeError("Type %s not serializable" % type(obj))


whois = Whois('unko.co.jp')
result = whois.get()

print(json.dumps(result, default=json_serial))
```

### use template file(ttp command)

```bash
$ git clone https://github.com/blacknon/pywhois2
$ cd pywhois2
$ whois google.jp | awk '/^# whois.jprs.jp/,/FAX番号/{print}' > /tmp/example.jp.txt
$ ttp -d /tmp/example.jp.txt -t ./pywhois2/templates/cctld/jp.tpl -o raw
[{'contact_zip_code': '94043', 'contact_email': 'dns-admin@google.com', 'contact_name': 'Google LLC', 'contact_name_local': 'Google LLC', 'updated': datetime.datetime(2023, 6, 1, 1, 5, 7, tzinfo=datetime.timezone(datetime.timedelta(seconds=32400))), 'expiration': datetime.datetime(2024, 5, 31, 0, 0, tzinfo=datetime.timezone(datetime.timedelta(seconds=32400))), 'created': datetime.datetime(2005, 5, 30, 0, 0, tzinfo=datetime.timezone(datetime.timedelta(seconds=32400))), 'registrant_name': 'Google LLC', 'registrant_name_local': 'Google LLC', 'domain_name': 'google.jp', 'name_servers': ['ns1.google.com', 'ns2.google.com', 'ns3.google.com', 'ns4.google.com'], 'status': {'ok': True, 'hold': False, 'to_be_suspended': False, 'suspended': False}, 'contact_address': 'Mountain View, 1600 Amphitheatre Parkway, CA', 'contact_fax': '16502530001', 'contact_phone': '16502530000', 'contact_address_local': 'Mountain View 1600 Amphitheatre Parkway CA'}]
```
