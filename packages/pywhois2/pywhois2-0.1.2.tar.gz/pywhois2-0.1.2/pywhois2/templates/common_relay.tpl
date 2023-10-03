<group>
   Domain Name: {{ domain_name | lower }}

   Registry Domain ID: {{ registry_domain_id | lower }}
   Registrar WHOIS Server: {{ registrar_whois_server | lower }}
   Registrar URL: {{ registrar_whois_url | lower }}

   Updated Date: {{ updated | ORPHRASE }}
   Creation Date: {{ creation | ORPHRASE }}
   Registry Expiry Date: {{ expiration | ORPHRASE }}

   Registrar:  {{ registrar_name | ORPHRASE }}
   Registrar IANA ID:  {{ registrar_id }}
   Registrar Abuse Contact Email: {{ registrar_email }}
   Registrar Abuse Contact Phone: {{ registrar_phone }}

   Domain Status: {{ domain_status | ORPHRASE | joinmatches("\n") }}

   Name Server: {{ name_servers | ORPHRASE | to_list | joinmatches }}

   DNSSEC: {{ dnssec | ORPHRASE }}
</group>
