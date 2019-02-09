#!/usr/bin/python

from ansible.module_utils.basic import *
import json
import ast

def main():

    fields = {
        "payload": {"required": True, "type": "str"},
        "new_database": {"required": True, "type": "str"}
    }

    module = AnsibleModule(argument_spec=fields)
    payload = ast.literal_eval(module.params["payload"])
    payload['database'] = module.params["new_database"]
    #payload["_hack"] = "null"

    module.exit_json(changed=True, updated_payload=payload, id=payload['id'])

if __name__ == '__main__':
    main()
