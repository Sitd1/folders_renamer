import copy
from pathlib import Path
from typing import Union

import pandas as pd
import re


class Renamer:

    def __init__(
            self,
            config: dict[Union[Path, str]],
    ):
        self.config = copy.deepcopy(config)
        self.folders_path = config.get('folders_path', None)
        self.excel_file_path = config.get('excel_file_path', None)
        self.filename_max_length = config.get('filename_max_length', 60)

        self.excel_skiprows = config.get('skiprows', None)
        self.excel_usecols = config.get('usecols', None)

        self.names_pattern_from_file = config.get('names_pattern_from_file', None)
        self.words_to_del = config.get('words_to_del', None)

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
        if self._names_counts_from_file is None:
            names_counts_from_file_ = dict()
            for name in self.names_from_excel.keys():
                nme = int(re.findall(self.names_pattern_from_file, name)[0])
                names_counts_from_file_[nme] = names_counts_from_file_.get(nme, 0) + 1
            self._names_counts_from_file = names_counts_from_file_
        return self._names_counts_from_file

    @property
    def merged_inform_from_file(self):
        if self._merged_inform_from_file is None:
            merged_names_from_file_ = dict()
            for name_from_excel in self.names_from_excel.keys():
                name_from_regex = int(re.findall(self.names_pattern_from_file, name_from_excel)[0])
                if merged_names_from_file_[name_from_regex] == 1:
                    val_len = self.filename_max_length
                else:
                    val_len = self.filename_max_length // self.names_counts_from_file[name_from_regex]
                val = ' '.join(re.findall(r"[A-Za-z\dа-яА-Яё\.]+", self.names_from_excel[name_from_excel]))[:val_len]
                merged_names_from_file_[name_from_regex] = merged_names_from_file_.get(name_from_regex, [])
                merged_names_from_file_[name_from_regex].append(val)
            self._merged_inform_from_file = merged_names_from_file_
        return self._merged_inform_from_file

    @property
    def full_names(self):
        if self._full_names is None:
            full_names_ = dict()
            for origin_name in self.origin_folder_names:
                for name_from_file in self.merged_inform_from_file:
                    if name_from_file in [int(i) for i in re.findall(r"(\d{2,})+", origin_name)]:
                        full_names_[origin_name] = full_names_.get(origin_name, [])
                        full_names_[origin_name].append(
                            ' '.join(self.merged_inform_from_file[name_from_file]).lower()
                        )
            self._full_names = full_names_
        return self._full_names

    @property
    def cleaned_names(self):
        if self._cleaned_names is None:
            cleaned_names_ = dict()
            for key, val in self.full_names.items():
                cleaned_names_[key] = ' '.join(val)
                if len(cleaned_names_[key]) > self.filename_max_length:
                    new_val, new_val_2 = [], []
                    for word in cleaned_names_[key].split():
                        new_word = word
                        if len(word) > 3:
                            new_word = word[:4]
                        if new_word not in new_val_2 and word not in self.words_to_del:
                            new_val_2.append(new_word)
                            new_val.append(word)
                            cleaned_names_[key] = ' '.join(new_val)
            self._cleaned_names = cleaned_names_
        return self._cleaned_names

    def rename(self):
        for path in self.folders_path.glob('*'):
            if path.is_dir():
                print(path.name)
                print(path)
                path.rename(self.folders_path / f'{path.name} - {self.cleaned_names[path.name]}')
