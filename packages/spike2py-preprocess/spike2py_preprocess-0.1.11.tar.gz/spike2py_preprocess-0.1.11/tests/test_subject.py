import numpy as np

import pytest
from pytest import approx

from spike2py_preprocess import trial
from spike2py_preprocess import subject
from spike2py_preprocess import study
import spike2py


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


def test_subject_paths_create_method(tmp_path):
    paths = subject.SubjectPaths(tmp_path)
    paths.create()
    assert paths.raw == tmp_path / "raw"
    assert paths.proc == tmp_path / "proc"
    assert paths.figures == tmp_path / "figures" / "preprocess"


def test_preprocess_subject_no_subject_preprocess(sub01_paths, channels_file1):
    subject.subject(subject_path=sub01_paths.home)
    file1 = sub01_paths.proc / "conv_biphasic.pkl"
    file2 = sub01_paths.proc / "khz_biphasic.pkl"
    assert file1.exists()
    assert file2.exists()
    data1 = spike2py.trial.load(file1)
    data2 = spike2py.trial.load(file2)
    assert data1.channels == channels_file1
    assert data2.channels == [
        ("W_Ext", "waveform"),
        ("Fdi", "waveform"),
        ("Stim", "waveform"),
    ]
    assert np.mean(data1.Fdi.values) == approx(-0.026770833935985772)
    file1.unlink()
    file2.unlink()


def test_preprocess_subject_with_subject_preprocess(sub02_paths):
    subject.subject(subject_path=sub02_paths.home)
    file1 = sub02_paths.proc / "conv_biphasic.pkl"
    file2 = sub02_paths.proc / "khz_biphasic.pkl"
    assert file1.exists()
    assert file2.exists()
    data1 = spike2py.trial.load(file1)
    assert np.mean(data1.Fdi.values) == approx(4.973229169271819)
    file1.unlink()
    file2.unlink()
