<group>
   Domain Name: {{ domain_name | lower }}

   Registry Domain ID: {{ registry_domain_id | lower }}
   Registrar WHOIS Server: {{ registrar_whois_server | lower }}
   Registrar URL: {{ registrar_whois_url | lower }}

   Updated Date: {{ updated | _line_ | strip('\n') | strip('\r') }}
   Creation Date: {{ creation | _line_ | strip('\n') | strip('\r') }}
   Registry Expiry Date: {{ expiration | _line_ | strip('\n') | strip('\r') }}

   Registrar:  {{ registrar_name | _line_ | strip('\n') | strip('\r') }}
   Registrar IANA ID:  {{ registrar_id }}
   Registrar Abuse Contact Email: {{ registrar_email }}
   Registrar Abuse Contact Phone: {{ registrar_phone }}

   Domain Status: {{ domain_status | _line_ | strip('\n') | strip('\r') | joinmatches("\n") }}

   Name Server: {{ name_servers | _line_ | strip('\n') | strip('\r') | to_list | joinmatches }}

   DNSSEC: {{ dnssec | _line_ | strip('\n') | strip('\r') }}

   URL of the ICANN Whois Inaccuracy Complaint Form: https://www.icann.org/wicf/
</group>
