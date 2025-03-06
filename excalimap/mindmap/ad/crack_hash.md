# Crack hash

## LM (299bd128c1101fd6)
- `john --format=lm hash.txt --wordlist=<rockyou.txt>`
- `hashcat -m 3000 -a 0 hash.txt <rockyou.txt>`

## NT (b4b9b02e6f09a9bd760...)
- `john --format=nt hash.txt --wordlist=<rockyou.txt>`
- `hashcat -m 1000 -a 0 hash.txt <rockyou.txt>`

## NTLMv1 (user::85D5BC...)
- `john --format=netntlm hash.txt --wordlist=<rockyou.txt>`
- `hashcat -m 1000 -a 0 hash.txt <rockyou.txt>`
- crack.sh
[https://crack.sh/](https://crack.sh/)

## NTLMv2 (user::N46iSNek...)
- `john --format=netntlmv2 hash.txt --wordlist=<rockyou.txt>`
- `hashcat -m 5600 -a 0 hash.txt <rockyou.txt>`

## Kerberos 5 TGS ($krb5tgs$23$...)
- `john --format=krb5tgs hash.txt --wordlist=<rockyou.txt>`
- `hashcat -m 13100 -a 0 hash.txt <rockyou.txt>`

## Kerberos 5 TGS AES128 ($krb5tgs$17...)
- `hashcat -m 19600 -a 0 hash.txt <rockyou.txt>`

## Kerberos ASREP ($krb5asrep$23...)
- `hashcat -m 18200 -a 0 hash.txt <rockyou.txt>`

## MSCache 2 (very slow) ($DCC2$10240...)
- `hashcat -m 2100 -a 0 hash.txt <rockyou.txt>`

## Timeroast hash ($sntp-ms$...)
- `hashcat -m 31300 -a 3 hash.txt -w 3 ?l?l?l?l?l?l?l `

## pxe hash ($sccm$aes128$...)
- `hashcat -m 19850 -a 0 hash.txt <rockyou.txt>`