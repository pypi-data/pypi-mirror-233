import json
import os
import re
import sys
from typing import Any, Dict
from pydantic import BaseModel


class GlobalConfigParser(BaseModel):
    id: str

    @classmethod
    def get_config(cls, env: str, json_config_filename="config.json", json_sub_dir='', **kwargs):
        mapper = kwargs
        subclass_path = sys.modules[cls.__module__].__file__
        json_dir = os.path.dirname(os.path.abspath(subclass_path))
        json_file = os.path.join(json_dir, json_sub_dir, json_config_filename)
        if not os.path.isfile(json_file):
            raise Exception(f"{json_config_filename} not exists in {json_dir}")
        override_key = 'overrides'
        with open(json_file) as f:
            json_config: Dict = json.load(f)
            env_config = {}
        if env in json_config:
            env_config = json_config[env]
        else:
            if not override_key in json_config or env not in json_config[override_key]:
                raise Exception(f"{env}: environment not found:")
            else:
                env_config = cls.__merge_environment(json_config['prod'], json_config[override_key][env])

        global_config_params = None
        if "global_config_params" in env_config.keys():
            global_config_params = env_config.pop("global_config_params")
        cls.__replace_env_placeholders(env_config, env, mapper, global_config_params)
        return cls.parse_obj(env_config)

    @classmethod
    def __merge_environment(cls, a, b) -> Dict:
        for key in b:
            if key in a:
                if isinstance(a[key], dict) and isinstance(b[key], dict):
                    cls.__merge_environment(a[key], b[key])
                else:
                    a[key] = b[key]
            else:
                a[key] = b[key]
        return a

    @classmethod
    def __replace_env_placeholders(
            cls, json_dict: Dict, env: str, mapper: dict[str, Any],
            global_config_params: Dict[str, Any]) -> Dict:
        for key in json_dict:
            if isinstance(json_dict[key], dict):
                cls.__replace_env_placeholders(json_dict[key], env, mapper, global_config_params)
            elif isinstance(json_dict[key], list):
                for index, item in enumerate(json_dict[key]):
                    if isinstance(item, dict):
                        cls.__replace_env_placeholders(item, env, mapper, global_config_params)
                    else:
                        if not isinstance(item, str):
                            continue
                        if item[0] == "#" and item[-1] == "#":
                            if item[1: -1] not in global_config_params:
                                raise Exception("global_config_params attribute is missing!")
                            json_dict[key][index] = global_config_params[item[1: -1]]
                            continue
                        ret_val = cls.__replace_env_placeholder('<env>', item, env)
                        for placeholder, value in mapper.items():
                            if f"<{placeholder}>" in ret_val:
                                ret_val = cls.__replace_env_placeholder(f"<{placeholder}>", ret_val, value)
                        json_dict[key][index] = ret_val
            else:
                if not isinstance(json_dict[key], str):
                    continue
                if json_dict[key][0] == "#" and json_dict[key][-1] == "#":
                    if json_dict[key][1: -1] not in global_config_params:
                        raise Exception("global_config_params attribute is missing!")
                    json_dict[key] = global_config_params[json_dict[key][1: -1]]
                    continue
                ret_val = cls.__replace_env_placeholder('<env>', json_dict[key], env)
                for placeholder, value in mapper.items():
                    if f"<{placeholder}>" in ret_val:
                        ret_val = cls.__replace_env_placeholder(f"<{placeholder}>", ret_val, value)
                json_dict[key] = ret_val

    @classmethod
    def __replace_env_placeholder(cls, pattern: str, string: str, repl: str) -> Any:
        if not isinstance(string, str):
            return string
        return re.sub(pattern, repl, string)
