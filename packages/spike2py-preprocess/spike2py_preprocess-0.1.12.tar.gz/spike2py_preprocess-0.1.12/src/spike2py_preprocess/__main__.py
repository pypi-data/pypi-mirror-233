from pathlib import Path

import typer

import spike2py_preprocess.study as study_
import spike2py_preprocess.subject as subject_
import spike2py_preprocess.trial as trial_
import spike2py_preprocess.utils as utils


app = typer.Typer(
    name="spike2py_preprocess", help="Preprocess Spike2 data exported to .mat."
)


@app.command()
def trial(trial_info_json: Path, plot: bool = False):
    """Preprocess trial

    trial_info_json: Path to json file containing details required by spike2py.trial.TrialInfo

    Sample json file
    ----------------
    {
    "file": "/home/maple/study1/sub01/raw/sub01_DATA000_H_B.mat",
    "channels": ["FDI", "W_EXT", "stim"],
    "name": "biphasic_high_fq",
    "subject_id": "sub01",
    "path_save_trial": "/home/maple/study1/sub01/proc",
    "path_save_figures": "/home/maple/study1/sub01/figures",
    }
    """
    trial_info = utils.get_trial_info(trial_info_json)
    trial_.trial(trial_info, plot=plot)


@app.command()
def subject(subject_path: str, plot: bool = False):
    """Preprocess all trials for a subject

    subject_path: path to subject folder
    """
    subject_.subject(subject_path, plot=plot)


@app.command()
def study(study_path, plot: bool = False):
    """Preprocess all trials from all subjects for a study

    study_path: path to study folder"""
    study_.study(study_path, plot=plot)


if __name__ == "__main__":
    app()
