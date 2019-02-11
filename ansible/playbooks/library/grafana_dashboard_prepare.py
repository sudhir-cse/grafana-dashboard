#!/usr/bin/python

from ansible.module_utils.basic import *
from ansible.module_utils._text import to_native
import json
import ast

def grafana_update_dashboard_version(dashboard, version):
    dashboard['dashboard']['version'] = version
    return dashboard

def grafana_panels_update_datasource(dashboard, datasource):
    for panel in dashboard['dashboard']['panels']:
        try:
            if panel['datasource']:
                print("Updating dashboard: {}, panel: {}".format(
                    dashboard['dashboard']['title'], panel['title']))
                panel['datasource'] = datasource
                print("updated: " +  panel['datasource'] + " >> " + datasource)

        except KeyError:
            print("Skipping dashboard: {}, panel: {}".format(
                dashboard['dashboard']['title'], panel['title']))
    return dashboard

def grafana_templating_update_datasource(dashboard, datasource):
    for item in dashboard['dashboard']['templating']['list']:
        try:
            if item['datasource']:
                print("Updating dashboard: {}, templating-item: {}".format(
                    dashboard['dashboard']['title'], item['label']))
                item['datasource'] = datasource
                print("updated: " +  item['datasource'] + " >>>> " + datasource)

        except KeyError:
            print("Dashboard: {}, templating-item: {} has no datasource field".format(
                dashboard['dashboard']['title'], item['label']))
    return dashboard

def main():

    fields = {
        "input_path": {"required": True, "type": "str"},
        "output_path": {"required": True, "type": "str"},
        "version": {"required": True, "type": "int"},
        "editable": {"required": True, "type": "bool"},
        "datasource": {"required": True, "type": "str"},
        "commit_message": {"required": True, "type": "str"},
        "overwrite": {"required": True, "type": "bool"} 
    }
    module = AnsibleModule(argument_spec=fields)
    
    try:
        with open(module.params['input_path'], 'r') as json_file:
            payload = json.load(json_file)
    except Exception as e:
        raise GrafanaAPIException("Can't load json file %s" % to_native(e))

    # Check that the dashboard JSON is nested under the 'dashboard' key
    if 'dashboard' not in payload:
        payload = {'dashboard': payload}

    payload["message"] = module.params["commit_message"]
    payload["overwrite"] = module.params["overwrite"]
    #payload['dashboard']['editable'] = module.params['editable']

    version_updated = grafana_update_dashboard_version(payload, module.params["version"])
    panels_datasource_updated = grafana_panels_update_datasource(version_updated, module.params["datasource"])
    templating_datasource_updated = grafana_templating_update_datasource(panels_datasource_updated, module.params["datasource"])
    templating_datasource_updated['dashboard']['editable'] = module.params['editable']

    with open(module.params['output_path'], 'w') as outfile:
        json.dump(templating_datasource_updated, outfile)

    module.exit_json(changed=True, dashboard=templating_datasource_updated)

if __name__ == '__main__':
    main()
