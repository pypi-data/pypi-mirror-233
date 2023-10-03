## Copyright (c) 2023 Blacknon. All rights reserved.
## Use of this source code is governed by an MIT license
## that can be found in the LICENSE file.
## =======================================================

## Macro
## =======================================================

<macro>
def standardize_status(data):
    if 'status' in data:
        if type(data['status']) == list:
            extract_data = data['status']
            del data['status']

            data['status'] = {
                'auto_renew_period': False,
                'inactive': False,
                'ok': False,
                'pending_create': False,
                'pending_delete': False,
                'pending_renew': False,
                'pending_restore': False,
                'pending_transfer': False,
                'pending_update': False,
                'redemption_period': False,
                'renew_period': False,
                'server_delete_prohibited': False,
                'server_hold': False,
                'server_renew_prohibited': False,
                'server_transfer_prohibited': False,
                'server_update_prohibited': False,
                'transfer_period': False,
                'client_delete_prohibited': False,
                'client_hold': False,
                'client_renew_prohibited': False,
                'client_transfer_prohibited': False,
                'client_update_prohibited': False,
            }

            for l in extract_data:
                line = " ".join(l.split(" ")[:-1]).lower()
                if line in ["ok", "active"]:
                    data['status']['ok'] = True
                elif line in ["auto_renew_period", "autorenewperiod"]:
                    data['status']['auto_renew_period'] = True
                elif line in ["inactive"]:
                    data['status']['inactive'] = True
                elif line in ["pending_create", "pendingcreate"]:
                    data['status']['pending_create'] = True
                elif line in ["pending_delete", "pendingdelete"]:
                    data['status']['pending_delete'] = True
                elif line in ["pending_renew", "pendingrenew"]:
                    data['status']['pending_renew'] = True
                elif line in ["pending_restore", "pendingrestore"]:
                    data['status']['pending_restore'] = True
                elif line in ["pending_transfer", "pendingtransfer"]:
                    data['status']['pending_transfer'] = True
                elif line in ["pending_update", "pendingupdate"]:
                    data['status']['pending_update'] = True
                elif line in ["redemption_period", "redemptionperiod"]:
                    data['status']['redemption_period'] = True
                elif line in ["renew_period", "renewperiod"]:
                    data['status']['renew_period'] = True
                elif line in ["server_delete_prohibited", "serverdeleteprohibited"]:
                    data['status']['server_delete_prohibited'] = True
                elif line in ["server_hold", "serverhold"]:
                    data['status']['server_hold'] = True
                elif line in ["server_renew_prohibited", "serverrenewprohibited"]:
                    data['status']['server_renew_prohibited'] = True
                elif line in ["server_transfer_prohibited", "servertransferprohibited"]:
                    data['status']['server_transfer_prohibited'] = True
                elif line in ["server_update_prohibited", "serverupdateprohibited"]:
                    data['status']['server_update_prohibited'] = True
                elif line in ["transfer_period", "transferperiod"]:
                    data['status']['transfer_period'] = True
                elif line in ["client_delete_prohibited", "clientdeleteprohibited"]:
                    data['status']['client_delete_prohibited'] = True
                elif line in ["client_hold", "clienthold"]:
                    data['status']['client_hold'] = True
                elif line in ["client_renew_prohibited", "clientrenewprohibited"]:
                    data['status']['client_renew_prohibited'] = True
                elif line in ["client_transfer_prohibited", "clienttransferprohibited"]:
                    data['status']['client_transfer_prohibited'] = True
                elif line in ["client_update_prohibited", "clientupdateprohibited"]:
                    data['status']['client_update_prohibited'] = True

    return data

def str2datetime(data):
    import datetime
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

<group macro="standardize_status, str2datetime">
Domain Name: {{ domain_name | ORPHRASE | lower }}
Registry Domain ID: {{ registry_domain_id | lower }}
Registrar WHOIS Server: {{ registrar_whois_server | lower }}
Registrar URL: {{ registrar_whois_url | lower }}
Last Modified: {{ updated | ORPHRASE }}
Registrar Name: {{ registrar_name | ORPHRASE }}
Registrar Abuse Contact Email: {{ registrar_email }}
Registrar Abuse Contact Phone: {{ registrar_phone }}
Reseller Name: {{ reseller_name | ORPHRASE }}
Status: {{ status | ORPHRASE | to_list | joinmatches }}
Status Reason: {{ status_reason | ORPHRASE }}
Registrant Contact ID: {{ registrant_id | ORPHRASE }}
Registrant Contact Name: {{ registrant_name | ORPHRASE }}
Tech Contact ID: {{ tech_id | ORPHRASE }}
Tech Contact Name: {{ tech_name | ORPHRASE }}
Name Server: {{ name_servers | lower | ORPHRASE | to_list | joinmatches }}
DNSSEC: {{ dnssec | ORPHRASE }}
Registrant: {{ registrant_organization | ORPHRASE }}
Eligibility Type: {{ eligibility_type | ORPHRASE }}
Eligibility Name: {{ eligibility_name | ORPHRASE }}
Eligibility ID: {{ eligibility_id | ORPHRASE }}

</group>
