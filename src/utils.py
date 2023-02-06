from typing import Union, Dict, Any
from pathlib import Path
import yaml


def get_config(path: Union[Path, str]) -> Dict[str, Any]:
    r"""Get anything what was in yaml. Probably dict"""
    with open(str(path), encoding='utf8') as conf_file:
        config = yaml.load(conf_file, Loader=yaml.Loader)
    return config
