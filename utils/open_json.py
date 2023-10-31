import json
import os


class OpenJson:

    @staticmethod
    def open_json(path):
        current_script_path = os.path.abspath(__file__)
        project_root_path = os.path.dirname(os.path.dirname(current_script_path)) + path
        with open(project_root_path, 'r') as json_file:
            data = json.load(json_file)
        return data
