#!/usr/bin/python

import json
import ast

payload = "{'withCredentials': False, 'basicAuthPassword': '', 'database': 'mydb', 'url': 'http://influxdb:8086', 'basicAuth': False, 'jsonData': {'keepCookies': []}, 'access': 'proxy', 'readOnly': True, 'typeLogoUrl': '', 'orgId': 1, 'user': '', 'version': 6, 'basicAuthUser': '', 'secureJsonFields': {}, 'password': '', 'type': 'influxdb', 'id': 2, 'isDefault': False, 'name': 'indb'}"

#payload = "{'a': 1, 'b': 2, 'c': 3}"

payload = ast.literal_eval(payload)
payload["d"] = 5

print(payload['database'])
print(payload['url'])
print(json.dumps(payload))