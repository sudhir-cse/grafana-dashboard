#!/usr/bin/python

from ansible.module_utils._text import to_native
import json
import ast

class GrafanaAPIException(Exception):
    pass


path = "/Users/sudhir/kpit-grafana/grafana-dashboard/ansible/grafana-dashboards/Apache-ds-test-1549815389342.json"
outputPath = "/Users/sudhir/kpit-grafana/grafana-dashboard/ansible/grafana-dashboards/Apache-ds-test-1549815389342-updated.json"
datasource = "indb"

try:
    with open(path, 'r') as json_file:
        dashboard = json.load(json_file)
        print(dashboard['title'])
except Exception as e:
    raise GrafanaAPIException("Can't load json file %s" % to_native(e))

# Update datasource in the panels
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

# Update datasource in the templating
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

with open(outputPath, 'w') as outfile:
    json.dump(dashboard, outfile)
