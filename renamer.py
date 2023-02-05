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
        for name in names_from_excel.keys():
            nme = int(re.findall(name_pattern_in_file, name)[0])
            if d_counts[nme] == 1:
                val_len = self.filename_max_length
            else:
                val_len = self.filename_max_length // self.names_counts_from_file[nme]
            val = ' '.join(re.findall(r"[A-Za-z0-9а-яА-Яё\.]+", names_from_excel[name]))[:val_len]
            merged_names_from_file_[nme] = merged_names_from_file_.get(nme, [])
            merged_names_from_file_[nme].append(val)
        return






def get_config(path: Union[Path, str]) -> Dict[str, Any]:
    r"""Get anything what was in yaml. Probably dict"""
    with open(str(path), encoding='utf8') as conf_file:
        exp_config = yaml.load(conf_file, Loader=yaml.Loader)
    return exp_config

df = pd.read_excel(excel_file_path, skiprows=6, usecols=[2, 3])
df.columns = [0, 1]

names_from_excel = df.set_index(0).dropna()[1].to_dict()

fpath = Path('//RU-MOWRAS005/Projects/_Project folders/2022 - Rostselmash - Budgeting control MTS/Client`s info')
folder_names = [el.name for el in fpath.glob("*") if el.is_dir()]

# names in file counts2
name_pattern_in_file = r"(\d+)"
d_counts = dict()
for name in names_from_excel.keys():
    nme = int(re.findall(name_pattern_in_file, name)[0])
    d_counts[nme] = d_counts.get(nme, 0) + 1




# merged inform in file2
names_edit = dict()
default_val_len = 60

for name in names_from_excel.keys():
    nme = int(re.findall(name_pattern_in_file, name)[0])
    val_len = default_val_len if d_counts[nme] == 1 else default_val_len // d_counts[nme]
    val = ' '.join(re.findall(r"[A-Za-z0-9а-яА-Яё\.]+", names_from_excel[name]))[:val_len]
    names_edit[nme] = names_edit.get(nme, [])
    names_edit[nme].append(val)

d_pre_res = dict()

for f_name in folder_names:
    for name in names_edit:
        if name in [int(i) for i in re.findall(r"(\d{2,})+", f_name)]:
            d_pre_res[f_name] = d_pre_res.get(f_name, [])
            d_pre_res[f_name].append(' '.join(names_edit[name]).lower())

d_res = dict()

to_del = ['по', 'в', 'и', 'на', 'с', 'для', 'от']

for key, val in d_pre_res.items():
    d_res[key] = ' '.join(val)
    if len(d_res[key]) > default_val_len:
        new_val, new_val_2 = [], []
        for word in d_res[key].split():
            new_word = word
            if len(word) > 3:
                new_word = word[:4]
            if new_word not in new_val_2 and word not in to_del:
                new_val_2.append(new_word)
                new_val.append(word)
                d_res[key] = ' '.join(new_val)

print('start renaming...')
for path in fpath.glob('*'):
    if path.is_dir():
        print(path.name)
        print(path)
        path.rename(fpath / f'{path.name} - {d_res[path.name]}')
        break

print('done!')
time.sleep(10)
print('closing')
for i in range(5,1):
    print(i)
    time.sleep(1)
