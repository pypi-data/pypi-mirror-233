import json
import os


class TargetSettingsFileReaderProtocol:

  def read_json_for(self, filepath):
    pass


class TargetSettingsFileReader(TargetSettingsFileReaderProtocol):

  def read_json_for(self, filepath: str) -> dict:

    if not filepath.endswith('.json'):
      raise Exception('Incorrect file format !')

    if not os.path.exists(filepath):
      raise Exception('File does not exist !')

    with open(filepath, 'r') as file_content:
      return json.load(file_content)
