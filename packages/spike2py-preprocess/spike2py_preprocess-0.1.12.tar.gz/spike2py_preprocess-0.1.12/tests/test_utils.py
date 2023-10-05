from pathlib import Path

import pytest

from spike2py_preprocess import utils


def test_read(study_details_json, study_details_dict):
    study_details = utils.read_json(study_details_json)
    assert study_details == study_details_dict


def test_read_FileNotFoundError_strict(capsys):
    file = Path("file.json")
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        utils.read_json(file)
    captured = capsys.readouterr()
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1
    assert captured.out == ("file.json does not exist.\n")


def test_read_FileNotFoundError_not_strict(capsys):
    file = Path("file.json")
    utils.read_json(file, strict=False)
    output = capsys.readouterr().out
    assert output == f"{file} does not exist.\n"


# TODO: Add test for new pdf merge function