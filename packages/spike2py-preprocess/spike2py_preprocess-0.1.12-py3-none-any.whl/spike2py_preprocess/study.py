from pathlib import Path

import spike2py_preprocess.utils as utils
import spike2py_preprocess.subject as subject


STUDY_INFO_FILE = "study_info.json"
STUDY_PREPROCESS_FILE = "study_preprocess.json"


def study(study_path: Path, plot=False):
    """Preprocess all trials from all subject for a study.

    The folder structure and the location of various `.json` files
    is prescriptive. If the structure is not correct, spike2py_preprocess
    will not work.

    Parameters
    ----------
    study_path: Top-level study folder
                study -> sub01 (other subjects at same level)
    plot: Flag of whether to generate plots of pickled sections

    """
    study_info = _get_study_info(study_path)
    print(f'Processing study: {study_info["name"]}')
    preprocess_info = utils.get_preprocess_info(study_path / STUDY_PREPROCESS_FILE)
    _process_study_subjects(study_path, study_info, preprocess_info, plot)


def _get_study_info(study_path):
    study_info = utils.read_json(study_path / STUDY_INFO_FILE)
    return study_info


def _process_study_subjects(study_path, study_info, preprocess_info, plot):
    for subject_ in study_info["subjects"]:
        subject.subject(study_path / subject_, preprocess_info, study_info, plot)
