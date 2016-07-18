#!/usr/bin/env python

import httplib
import urllib

headers = {
    "Content-Type": "application/json"
}

conn = httplib.HTTPConnection("localhost", 26000, True, 3)
conn.request("GET", "/ping?apikey=" + "8762d758-191b-47aa-bfd5-568c3ecdd45a", None)
res = conn.getresponse()
print res.status
print res.reason
print res.read()
