whitelist
=========

Generate a list of ipaddresses based off the SPF records of domain names.
This whitelist is intended for spamdb and pf

whitelist.py can generate a list of ip addresses for a domain name
```
fred$ ./whitelist.py -d google.com
173.194.0.0/16
2001:4860:4000::/36
. . .
74.125.0.0/16
```

or for a list of domain names.

```
fred$ ./bin/whitelist -f domains.txt
106.50.16.0/28
107.20.52.15
. . .
96.46.150.192/27
```

