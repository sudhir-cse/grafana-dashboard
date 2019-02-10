#!/usr/bin/python

from ansible.module_utils.basic import *
from ansible.module_utils._text import to_native
import json

class GrafanaDashboardException(Exception):
    pass

def main():

    fields = {
        "dashboard_json_path": {"required": True, "type": "str"}
    }

    module = AnsibleModule(argument_spec=fields)
    dashboard_json_path = module.params["dashboard_json_path"]
    
    # Parse for uid
    try:
        with open(dashboard_json_path, 'r') as json_file:
            dashboard = json.load(json_file)
            uid = dashboard['uid']
    except Exception as e:
        raise GrafanaDashboardException("Can't load json file %s" % to_native(e))

    module.exit_json(changed=True, uid=uid)

if __name__ == '__main__':
    main()
