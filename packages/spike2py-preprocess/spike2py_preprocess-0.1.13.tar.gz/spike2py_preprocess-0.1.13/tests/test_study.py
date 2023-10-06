import numpy as np

from pytest import approx

from spike2py_preprocess import study
import spike2py


def test_preprocess_study_no_subject_preprocess(study1_path, sub01_paths, sub02_paths):
    study.study(study1_path)
    file1 = sub01_paths.proc / "conv_biphasic.pkl"
    file2 = sub01_paths.proc / "khz_biphasic.pkl"
    assert file1.exists()
    assert file2.exists()
    data1 = spike2py.trial.load(file1)
    data2 = spike2py.trial.load(file2)
    channels = [("W_Ext", "waveform"), ("Fdi", "waveform"), ("Stim", "waveform")]
    assert data1.channels == channels
    assert data2.channels == channels
    assert np.mean(data1.Fdi.values) == approx(1.8046494617496535e-09)
    file3 = sub02_paths.proc / "conv_biphasic.pkl"
    file4 = sub02_paths.proc / "khz_biphasic.pkl"
    file1.unlink()
    file2.unlink()
    file3.unlink()
    file4.unlink()
