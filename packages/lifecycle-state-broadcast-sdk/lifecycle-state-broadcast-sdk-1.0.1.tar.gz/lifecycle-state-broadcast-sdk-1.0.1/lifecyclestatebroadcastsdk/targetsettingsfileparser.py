import json
import os
import re
import pathlib
import re

from jinja2 import Environment, FileSystemLoader


class TargetSettingsFileParser:

  def find_nodes_for_key(self, data, target_key, partial=False, path_filter=None):
    nodes = []
    target_key_lower = target_key.lower()

    def helper(d, path=''):
        if isinstance(d, dict):
            if partial:
                # Check if target_key_lower is a substring of any key
                if any(target_key_lower in k.lower() for k in d.keys()):
                    node_with_path = d.copy()
                    node_with_path['_path'] = path
                    if all(item not in path for item in (path_filter or [])):
                      nodes.append(node_with_path)
            else:
                # Check for exact match
                if target_key_lower in (k.lower() for k in d.keys()):
                    node_with_path = d.copy()
                    node_with_path['_path'] = path
                    if all(item not in path for item in (path_filter or [])):
                      nodes.append(node_with_path)
            for key, value in d.items():
                helper(value, f"{path}/{key}")

        elif isinstance(d, list):
            for index, item in enumerate(d):
                helper(item, f"{path}[{index}]")

    helper(data)
    return nodes

  def get_value(self, d, keys, default=''):
    normalized_keys = [key.lower() for key in keys]
    for k, v in d.items():
      if k.lower() in normalized_keys:
        return v
    return default

  def build_dependencies_with_default_props(self, nodes):
    result = []
    for n in nodes:
      result.append({
        'id': self.get_value(n, ['id', 'name']),
        "endpoint": self.get_value(n, ['endpoint', 'url', 'logendpoint', 'address', 'alertTriggerEndpoint']),
        "enpoints": ','.join(n.get('endpoints', n.get('servers'))) if len(n.get('endpoints', n.get('servers', []))) > 0 else '',
        "hostName": self.get_value(n, ['hostName', 'host']),
        "portNumber": self.get_value(n, ['port', 'portNumber']),
        '_path': n.get('_path')
        # '_meta': json.dumps(n)
      })
    return result

  def build_dependencies_with_pubsub_props(self, nodes):
    result = []
    for n in nodes:
      result.append({
        'id': self.get_value(n, ['id']),
        "projectId": self.get_value(n, ['projectid']),
        "topicId": self.get_value(n, ['topicid']),
        '_path': n.get('_path')
        # '_meta': json.dumps(n)
      })
    return result

  def build_dependencies_with_bigquery_props(self, nodes):
    result = []
    for n in nodes:
      result.append({
        'id': self.get_value(n, ['id']),
        "projectId": self.get_value(n, ['projectid']),
        "dataset": self.get_value(n, ['dataset']),
        "table": self.get_value(n, ['table']),
        '_path': n.get('_path')
        # '_meta': json.dumps(n)
      })
    return result

  def build_dependencies_with_mssql_props(self, nodes):

    result = []
    for n in nodes:
      val = self.get_value(n, ['onlinedataconnectionstring'], '')
      if val == '':
        return result
      match = re.search(r'Data Source=(?P<host>[^:;]+)(?::(?P<port>\d+))?', val)
      if match:
        hostname = match.group('host')
        port = match.group('port')  # This will be None if port is not specified
        result.append({
          'hostName': hostname,
          'portNumber': port or 1433,
          '_path': n.get('_path')
        })
    return result

  def discover_dependencies(self, d):
    nodes = [
      self.build_dependencies_with_default_props(self.find_nodes_for_key(d, 'host')),
      self.build_dependencies_with_default_props(self.find_nodes_for_key(d, 'hostname')),
      self.build_dependencies_with_default_props(self.find_nodes_for_key(d, 'url', path_filter=['websites', 'websities'])),
      self.build_dependencies_with_default_props(self.find_nodes_for_key(d, 'port')),
      self.build_dependencies_with_default_props(self.find_nodes_for_key(d, 'portnumber')),
      self.build_dependencies_with_default_props(self.find_nodes_for_key(d, 'servers')),
      self.build_dependencies_with_default_props(self.find_nodes_for_key(d, 'endpoint', partial=True, path_filter=['IpRateLimiting', 'application'])),
      self.build_dependencies_with_pubsub_props(self.find_nodes_for_key(d, 'topicid')),
      self.build_dependencies_with_bigquery_props(self.find_nodes_for_key(d, 'dataset')),
      self.build_dependencies_with_mssql_props(self.find_nodes_for_key(d, 'connectionstring', True)),
    ]
    cleaned_result = []
    for node in nodes:
      for n in node:
        cleaned_result.append(self.clean_dict(n))
    return json.dumps([dict(t) for t in {tuple(d.items()) for d in cleaned_result}])

  def parse(self, settings: dict, fallbacks: dict) -> dict:

    try:

      # lib_root_path = pathlib.Path(__file__).resolve().parent.parent.parent

      current_dir = os.path.dirname(os.path.abspath(__file__))
      templates_path = os.path.join(current_dir, 'templates')

      env = Environment(loader=FileSystemLoader(templates_path))
      env.filters['discover_dependencies'] = self.discover_dependencies
      template = env.get_template('default.j2')

      rendered_str = template.render({
        'settings': settings,
        'fallbacks': fallbacks
      })

      rendered_json = json.loads(re.sub(r',\s*}', '}', re.sub(r',\s*]', ']', rendered_str)))

    except Exception as e:
      return {
        'error': e
      }
    #cleaned_depends_on = []
    #if len(rendered_json.get('dependsOn', [])) > 0:
    #  for d in rendered_json.get('dependsOn'):
    #    cleaned_depends_on.append(self.clean_dict(d))
    #rendered_json['dependsOn'] = [dict(t) for t in {tuple(d.items()) for d in cleaned_depends_on}]
    return rendered_json

  def clean_dict(self, d):
    if not isinstance(d, dict):
      return d

    cleaned = {}
    for key, value in d.items():
      if key == 'id':
        cleaned[key] = value
      elif value not in ['', None, -1]:
        cleaned_value = self.clean_dict(value)
        if cleaned_value not in ['', None, -1]:
          cleaned[key] = cleaned_value

    return cleaned
