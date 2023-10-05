import sys
import json
from pathlib import Path
from typing import Union
import shutil

from PyPDF2 import PdfMerger

import spike2py


def read_json(json_path: Path, strict: bool = True) -> Union[dict, None]:
    """
    Read json file and return its content.

    If strict=True and file not found, program will stop.
    If strict=False and file note found, program will continue.

    Parameters
    ----------
    json_path
        Full-path to json file
    strict
        Set behaviour if file not found

    Raises
    ------
    FileNotFoundError

    Returns
    -------
    dict
        Content of json file.
    None
        When file not found and strict=False.
    """
    try:
        with open(json_path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        message = f"{json_path} does not exist."
        print(message)
        if strict:
            sys.exit(1)
        return


def get_trial_info(trial_info_json: Path) -> spike2py.trial.TrialInfo:
    """Retrieve trial info from json and return spike2py TrialInfo object"""
    trial_info_dict = read_json(trial_info_json)
    trial_info_dict = _convert_to_paths(trial_info_dict)
    trial_info = spike2py.trial.TrialInfo(**trial_info_dict)
    return trial_info


def _convert_to_paths(trial_info_dict):
    trial_info_dict["file"] = Path(trial_info_dict["file"])
    trial_info_dict["path_save_trial"] = Path(trial_info_dict["path_save_trial"])
    trial_info_dict["path_save_figures"] = Path(trial_info_dict["path_save_figures"])
    return trial_info_dict


def get_preprocess_info(preprocess_file, preprocess_info=None):
    """Get preprocess info for current file, if it exists

    Preprocess details can be passed down from the study level, or the
    subject level. But if there is preprocessing details specific to a
    given trial, it overrides the subject and study preprocessing details."""
    if preprocess_file.exists():
        return read_json(preprocess_file)
    else:
        return preprocess_info


def merge_pdfs(path):
    merger = PdfMerger()
    temp = path / 'temp'
    temp.mkdir()
    for item in path.iterdir():
        if item.suffix == '.pdf':
            temp_file = temp / (item.stem + '.pdf')
            merger.append(item)
            print(f'adding {item}')
            item.rename(temp_file)
    merger.write(path / (path.parent.parent.stem + '.pdf'))
    merger.close()
    shutil.rmtree(temp)
