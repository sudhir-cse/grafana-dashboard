#!/usr/bin/python

from ansible.module_utils.basic import *
from ansible.module_utils._text import to_native
import json
import ast

def grafana_update_dashboard_version(dashboard, version):
    dashboard['version'] = version
    return dashboard

def grafana_panels_update_datasource(dashboard, datasource):
    for panel in dashboard['panels']:
        try:
            if panel['datasource']:
                print("Updating dashboard: {}, panel: {}".format(
                    dashboard['title'], panel['title']))
                panel['datasource'] = datasource
                print("updated: " +  panel['datasource'] + " >> " + datasource)

        except KeyError:
            print("Skipping dashboard: {}, panel: {}".format(
                dashboard['title'], panel['title']))
    return dashboard

def grafana_templating_update_datasource(dashboard, datasource):
    for item in dashboard['templating']['list']:
        try:
            if item['datasource']:
                print("Updating dashboard: {}, templating-item: {}".format(
                    dashboard['title'], item['label']))
                item['datasource'] = datasource
                print("updated: " +  item['datasource'] + " >>>> " + datasource)

        except KeyError:
            print("Dashboard: {}, templating-item: {} has no datasource field".format(
                dashboard['title'], item['label']))
    return dashboard

def main():

    fields = {
        "input_path": {"required": True, "type": "str"},
        "output_path": {"required": True, "type": "str"},
        "version": {"required": True, "type": "int"},
        "editable": {"required": True, "type": "bool"},
        "datasource": {"required": True, "type": "str"} 
    }
    module = AnsibleModule(argument_spec=fields)
    
    try:
        with open(module.params['input_path'], 'r') as json_file:
            dashboard = json.load(json_file)

    except Exception as e:
        raise GrafanaAPIException("Can't load json file %s" % to_native(e))

    version_updated = grafana_update_dashboard_version(dashboard, module.params["version"])
    panels_datasource_updated = grafana_panels_update_datasource(version_updated, module.params["datasource"])
    templating_datasource_updated = grafana_templating_update_datasource(panels_datasource_updated, module.params["datasource"])
    templating_datasource_updated['editable'] = module.params['editable']

    # payload = ast.literal_eval(module.params["payload"])
    # payload['database'] = module.params["new_database"]
    # payload['readOnly'] = False
    # #payload["_hack"] = "null"

    with open(module.params['output_path'], 'w') as outfile:
        json.dump(templating_datasource_updated, outfile)

    module.exit_json(changed=True, dashboard=templating_datasource_updated)

if __name__ == '__main__':
    main()
