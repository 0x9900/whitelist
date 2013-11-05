#!/usr/bin/env python
#
# Author: Fred C.
# Email:
#
from __future__ import print_function

import DNS
import re
import sys

from collections import defaultdict

USAGE = """
whitelist.py [-d domain.tld | -f domain_list.txt]
"""

RE_PARSE = re.compile(r'(ip4|ip6|include|redirect)[:=](.*)', re.IGNORECASE)
MAX_RECURSION = 5

def dns_txt(domain):
  try:
    resp = DNS.dnslookup(domain, 'TXT')
  except DNS.ServerError as err:
    print(err, file=sys.stderr)
    return None

  response = []
  for r in resp:
    response.append(''.join(r))
  return response

def dns_parse(txt_field):
  resp = defaultdict(set)
  for rec in txt_field:
    fields = rec.split()
    for field in fields:
      match = RE_PARSE.match(field)
      if match:
        resp[match.group(1)].add(match.group(2))

  return resp

def process(domain):
  domains = [domain]
  ip_addresses = set()
  for cnt in range(MAX_RECURSION):
    includes = set()
    for dom in domains:
      txt = dns_txt(dom)
      if not txt:
        continue
      spf = dns_parse(txt)
      ip_addresses |= spf.get('ip4', set())
      ip_addresses |= spf.get('ip6', set())
      includes |= spf.get('include', set())
      includes |= spf.get('redirect', set())
    if not includes:
      break
    domains = includes
  return ip_addresses

if __name__ == '__main__':
  whitelist = set()
  if len(sys.argv) != 3 or sys.argv[1] not in ('-f', '-d'):
    print('Wrong arguments', file=sys.stderr)
    print(USAGE, file=sys.stderr)
    sys.exit(1)

  if sys.argv[1] == '-d':
    for ip in process(sys.argv[2]):
      whitelist.add(ip)
  elif sys.argv[1] == '-f':
    with open(sys.argv[2]) as fd:
      for line in fd:
        line = line.strip()
        for ip in process(line):
          whitelist.add(ip)

  for ip in sorted(whitelist):
    print(ip)
