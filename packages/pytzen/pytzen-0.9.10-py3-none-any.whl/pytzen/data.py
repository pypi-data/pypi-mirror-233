import os
import sys
import json
import copy

class DataStore:
    
    def __init__(self) -> None:
        self.config_json_path = os.environ.get('CONFIG_JSON_PATH', '.')
        self.config = self._generate_config()

    def _get_json(self, json_path):
        with open(json_path, 'r') as file:
            return json.load(file)

    def _get_args(self):
        arg_dict = {}
        for arg in sys.argv[1:]:
            if arg.startswith('--'):
                key, value = arg[2:].split('=')
                arg_dict[key] = value
        return arg_dict

    def _get_env(self, config_dict):
        env_dict = {}
        for key in config_dict.keys():
            if os.environ.get(key.upper()):
                env_dict[key] = os.environ.get(key.upper())
        return env_dict

    def _generate_config(self):
        config_dict = self._get_json(self.config_json_path)
        arg_dict = self._get_args()
        env_dict = self._get_env(config_dict)
        output_config = {}
        for var_name, default_value in config_dict.items():
            env_val = env_dict.get(var_name, default_value)
            final_val = arg_dict.get(var_name, env_val)
            output_config[var_name] = final_val
        return output_config
    
def update_config(doc:str, class_name:str, data:DataStore):
    original_config = copy.deepcopy(data.config)
    if 'classes' not in data.config:
        data.config['classes'] = {}
    data.config['classes'][class_name] = doc
    data_att = {a: type(v).__name__ 
                for a, v in data.__dict__.items() 
                if not callable(getattr(data, a)) 
                and not a.startswith('_')}
    data.config['data'] = data_att
    if data.config != original_config:
        with open(data.config_json_path, 'w') as json_file:
            json.dump(data.config, json_file, indent=4, 
                      ensure_ascii=False, separators=(',', ': '))