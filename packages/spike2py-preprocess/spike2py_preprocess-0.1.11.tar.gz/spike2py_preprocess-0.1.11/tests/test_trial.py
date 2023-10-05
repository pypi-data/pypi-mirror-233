from pathlib import Path

import pytest
import numpy as np
from pytest import approx

from spike2py_preprocess import trial
import spike2py
from spike2py.trial import TrialInfo


def test_preprocess_trial_no_trial_preprocess(sub1_trial_info, temp_path):
    trial.trial(sub1_trial_info)
    pkl_file = temp_path / (sub1_trial_info.name + ".pkl")
    assert pkl_file.exists()
    data = spike2py.trial.load(pkl_file)
    assert np.mean(data.Fdi.values) == approx(-0.02452170146926789)


def test_preprocess_trial_with_trial_preprocess(sub2_trial_info, temp_path):
    trial.trial(sub2_trial_info)
    pkl_file = temp_path / (sub2_trial_info.name + ".pkl")
    assert pkl_file.exists()
    data = spike2py.trial.load(pkl_file)
    assert np.mean(data.W_Ext.values) == approx(-1.9762610940015095)


def test_preprocess_trial_with_subject_preprocess(
    sub1_trial_info, temp_path, subject_preprocess_details
):
    trial.trial(sub1_trial_info)
    pkl_file = temp_path / (sub1_trial_info.name + ".pkl")
    assert pkl_file.exists()


def test_channel_not_present_for_preprocess(
    sub1_data, study_preprocess_details_wrong, attribute_error_message, capsys
):
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        trial._preprocess_data(sub1_data, study_preprocess_details_wrong)
    captured = capsys.readouterr()
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1
    assert captured.out == attribute_error_message


def test_check_paths_trial_info():
    trial_info = TrialInfo(
        file=Path("/home/maple/study1/sub01/raw/01_DATA_000_C_B.mat"),
        name="mvc_4",
        subject_id="sub01",
    )
    trial_info = trial._check_paths_trial_info(trial_info)
    figure_save = "/home/maple/study1/sub01/figures"
    assert str(trial_info.path_save_figures) == figure_save


def test_trial_trial_with_sections(section_file_path):
    trial_info = TrialInfo(
        file=section_file_path,
        name="mvc_4",
        subject_id="sub01",
    )
    trial.trial(trial_info)
    proc_save = section_file_path.parent.parent / "proc"

    mmax_data = proc_save / "mvc_4_mmax.pkl"
    ramp_data = proc_save / "mvc_4_ramp.pkl"
    threshold_data = proc_save / "mvc_4_threshold.pkl"
    assert mmax_data.exists()
    assert ramp_data.exists()
    assert threshold_data.exists()

    mmax_data.unlink()
    ramp_data.unlink()
    threshold_data.unlink()
