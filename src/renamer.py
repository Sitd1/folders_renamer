import copy
import time
from pathlib import Path
from typing import Union, Dict

import pandas as pd
import re

import yaml

class Renamer:

    def __init__(
            self,
            config: Union[Path, str],
    ):
        self.config = copy.deepcopy(config)
        self.folders_path = config.get('folders_path', None)
        self.excel_file_path = config.get('excel_file_path', None)
        self.filename_max_length = config.get('filename_max_length', 60)

        self.excel_skiprows = config.get('skiprows', None)
        self.excel_usecols = config.get('usecols', None)

        self.names_pattern_from_file = config.get('names_pattern_from_file', None)
        self.words_to_del = config.get('names_pattern_from_file', None)

        self._names_from_excel = None
        self._origin_folder_names = None
        self._names_counts_from_file = None
        self._merged_inform_from_file = None
        self._full_names = None
        self._cleaned_names = None


    @property
    def origin_folder_names(self):
        if self._origin_folder_names is None:
            self._origin_folder_names = [
                el.name for el in self.folders_path.glob("*") if el.is_dir()
            ]
            return self._origin_folder_names

    @property
    def names_from_excel(self) -> pd.Series:
        if self._names_from_excel is None:
            df = pd.read_excel(self.excel_file_path,
                               skiprows=self.excel_skiprows,
                               usecols=self.excel_usecols
                               )
            df.columns = [0, 1]
            self._names_from_excel = df.set_index(0).dropna()[1].to_dict()
            return self._names_from_excel

    @property
    def names_counts_from_file(self) -> dict:
        names_counts_from_file_ = dict()
        for name in names_from_excel.keys():
            nme = int(re.findall(name_pattern_in_file, name)[0])
            names_counts_from_file_[nme] = d_counts.get(nme, 0) + 1
        self._names_counts_from_file = names_counts_from_file_
        return self._names_counts_from_file

    @property
    def merged_inform_from_file(self):
        merged_names_from_file_ = dict()
        for name_from_excel in names_from_excel.keys():
            name_from_regex = int(re.findall(name_pattern_in_file, name_from_excel)[0])
            if d_counts[name_from_regex] == 1:
                val_len = self.filename_max_length
            else:
                val_len = self.filename_max_length // self.names_counts_from_file[name_from_regex]
            val = ' '.join(re.findall(r"[A-Za-z0-9а-яА-Яё\.]+", names_from_excel[name_from_excel]))[:val_len]
            merged_names_from_file_[name_from_regex] = merged_names_from_file_.get(name_from_regex, [])
            merged_names_from_file_[name_from_regex].append(val)
        self._merged_names_from_file = merged_names_from_file_
        return self._merged_names_from_file

    @property
    def full_names(self):
        if self._full_names is None:
            for origin_name in self.origin_folder_names:
                for name_from_file in self.merged_inform_from_file:
                    if name_from_file in [int(i) for i in re.findall(r"(\d{2,})+", origin_name)]:
                        d_pre_res[origin_name] = d_pre_res.get(origin_name, [])
                        d_pre_res[origin_name].append(' '.join(names_edit[name_from_file]).lower())

    def rename(self):
        for path in self.folders_path.glob('*'):
            if path.is_dir():
                print(path.name)
                print(path)
                path.rename(fpath / f'{path.name} - {d_res[path.name]}')

def get_config(path: Union[Path, str]) -> Dict[str, Any]:
    r"""Get anything what was in yaml. Probably dict"""
    with open(str(path), encoding='utf8') as conf_file:
        exp_config = yaml.load(conf_file, Loader=yaml.Loader)
    return exp_config

print('done!')
time.sleep(10)
print('closing')
for i in range(5,1):
    print(i)
    time.sleep(1)
