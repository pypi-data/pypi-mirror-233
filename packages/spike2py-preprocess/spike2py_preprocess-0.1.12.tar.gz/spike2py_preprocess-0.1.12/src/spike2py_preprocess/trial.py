import sys
from typing import Union


import spike2py as s2p
import spike2py_preprocess.utils as utils
import spike2py_preprocess.trial_sections as trial_sections


def trial(
    trial_info: s2p.trial.TrialInfo,
    preprocess_info: Union[dict, None] = None,
    plot=False,
):
    """Read, preprocess, section and save data to pickle

    Preprocess is not required, but is applied if provided.
    If TextMark channel exists indicating sections in trial,
    these will be extracted and saved. If no sections are present,
    the entire trial is saved.

    Parameters
    ----------
    trial_info: TrialInfo
        Instance of spike2py TrialInfo with info required to load data
    preprocess_info: dict | None
        If provided, details of what channels to preprocess and how to process them.
        Example:
        {"Fdi": {
            "remove_mean": "",
            "lowpass": "cutoff=100"}
        }
    """
    preprocess_file = trial_info.file.parent / f"preprocess_{trial_info.file.stem}.json"
    preprocess_info = utils.get_preprocess_info(preprocess_file, preprocess_info)
    data = _get_data(trial_info)
    data = _preprocess_data(data, preprocess_info)
    if plot:
        plot_data(data)
    if _trial_sections_exist(data):
        trial_sections.extract(data, plot)
    else:
        data.save()
        print(f"\t\tSaved {data.info.name}.pkl")


def _get_data(trial_info):
    trial_info = _check_paths_trial_info(trial_info)
    try:
        data = s2p.trial.Trial(trial_info)
    except FileNotFoundError:
        print(f"Unable to read {trial_info.file}. Please make sure it exists.")
        sys.exit(1)
    return data


def _check_paths_trial_info(trial_info: s2p.trial.TrialInfo):
    if trial_info.path_save_trial is None:
        trial_info.path_save_trial = trial_info.file.parent.parent / "proc"

    if trial_info.path_save_figures is None:
        trial_info.path_save_figures = trial_info.file.parent.parent / "figures"
    return trial_info


def _preprocess_data(data, preprocess_info):
    if _preprocess_required(preprocess_info):
        data = _preprocess(data, preprocess_info)
        print(f"\t\tPreprocessing {data.info.name}")
    return data


def _preprocess_required(preprocess_info):
    return preprocess_info is not None


def plot_data(data):
    try:
        data.plot(save=True)
    except AttributeError:
        print(
            f"\t\tPlot for trial {data.info.file.stem} not created. "
            f"\n\t\tMissing attributes in spike2py.trial.TrialFile object"
            f"\n\t\t\tname = {data.info.name}"
            f"\n\t\t\tsub_id = {data.info.subject_id}"
        )


def _preprocess(data, preprocess_info):
    """Preprocess each channel specified in preprocess_info.

    Each preprocessing step is specified with relevant arguments;
    these are applied to the relevant channels."""
    for channel, preprocesses in preprocess_info.items():
        for preprocess_name, preprocess_arguments in preprocesses.items():
            try:
                exec(f"data.{channel}.{preprocess_name}({preprocess_arguments})")
            except AttributeError:
                print(
                    f"Following spike2py data does not have requested attribute: \n"
                    f"\tdata.{channel}.{preprocess_name}({preprocess_arguments})\n"
                    f"{data.info.name}"
                )
                sys.exit(1)
    return data


def _trial_sections_exist(data):
    return ("Memory", "textmark") in data.channels
