import copy

import pytest
import numpy as np

from spike2py_preprocess import trial_sections


def test_get_section_details(data_with_sections):
    section_names, section_times = trial_sections._get_section_details(
        data_with_sections
    )
    expected_names = ["mmax", "mmax", "threshold", "threshold", "ramp", "ramp"]
    expected_times = np.array(
        [146.5533, 254.420703, 796.434507, 880.762869, 1503.990216, 1570.510863]
    )
    assert section_names == expected_names
    assert section_times == pytest.approx(expected_times)


def test_get_section_details(data_with_sections):
    section_names = ["mmax", "mmax", "threshold", "threshold", "ramp", "ramp"]
    assert trial_sections._validate_sections(section_names, data_with_sections) == None


def test_validate_file_is_path(data_with_sections, not_path_error_message, capsys):
    data_with_sections.info.file = ""
    section_names = ["mmax", "mmax", "threshold", "threshold", "ramp", "ramp"]
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        trial_sections._validate_sections(section_names, data_with_sections)
    captured = capsys.readouterr()
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1
    assert captured.out == not_path_error_message


def test_validate_even_sections(
    data_with_sections, uneven_textmarks_error_message, capsys
):
    section_names = ["mmax", "mmax", "MVC", "threshold", "threshold", "ramp", "ramp"]
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        trial_sections._validate_sections(section_names, data_with_sections)
    captured = capsys.readouterr()
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1
    assert captured.out == uneven_textmarks_error_message


def test_validate_matching_section_names(
    data_with_sections, non_matching_section_names_error_message, capsys
):
    section_names = ["mmax", "mmx", "threshold", "threshold", "ramp", "ramp"]
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        trial_sections._validate_sections(section_names, data_with_sections)
    captured = capsys.readouterr()
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1
    assert captured.out == non_matching_section_names_error_message


def test_concat_section_names_times():
    section_names = ["mmax", "mmax", "threshold", "threshold", "ramp", "ramp"]
    section_times = np.array(
        [146.5533, 254.420703, 796.434507, 880.762869, 1503.990216, 1570.510863]
    )
    section_name_times = trial_sections._concat_section_names_times(
        section_names, section_times
    )
    expected_section_name_times = {
        "mmax": [146.5533, 254.420703],
        "ramp": [1503.990216, 1570.510863],
        "threshold": [796.434507, 880.762869],
    }
    assert section_name_times == pytest.approx(expected_section_name_times)


def test_remove_memory_channel(data_with_sections):
    # Confirm channels include "Memory"
    channels_before = data_with_sections.channels
    memory_present = False
    for channel_name, _ in channels_before:
        print(channel_name)
        if channel_name == "Memory":
            memory_present = True
            break
    assert memory_present
    # Confirm channels no longer have "Memory"
    channels_after = trial_sections._remove_memory_channel(channels_before)
    memory_present = False
    for channel_name, _ in channels_after:
        if channel_name == "Memory":
            memory_present = True
            break
    assert not memory_present


def test_get_section_time_indexes(data_with_sections):
    section_times = [146.5533, 254.420703]
    channel_name = "Sol"
    time_indexes = trial_sections._get_section_time_indexes(
        data_with_sections, channel_name, section_times
    )
    assert time_indexes == [290779, 504802]


@pytest.mark.parametrize(
    "channel_attr, len_new_times",
    [("times", 214023), ("values", 214023), ("raw_values", 214023)],
)
def test_get_section_waveform_for(data_with_sections, channel_attr, len_new_times):
    # Confirm length of original Sol data
    assert len(data_with_sections.Sol.times) == 3776020
    time_indexes = [290779, 504802]
    channel_name = "Sol"
    new_times = trial_sections._get_waveform_section_for(
        "times", data_with_sections, channel_name, time_indexes
    )
    assert len(new_times) == len_new_times


@pytest.mark.parametrize(
    "channel_attr, len_new_times",
    [("times", 42000), ("values", 42000), ("raw_values", 42000)],
)
def test_get_section_waveform_for_multiple_time_indexes(
    data_with_sections, channel_attr, len_new_times
):
    time_indexes = [290779, 292779, 464802, 504802]
    channel_name = "Sol"
    new_times = trial_sections._get_waveform_section_for(
        channel_attr, data_with_sections, channel_name, time_indexes
    )
    assert len(new_times) == len_new_times


@pytest.mark.parametrize(
    "section_times, len_new_times",
    [([146, 254], 6), ([0, 10], 0)],
)
def test_get_section_event(data_with_sections, section_times, len_new_times):
    # Confirm length of original Sol data
    assert len(data_with_sections.Mmax.times) == 14
    channel_name = "Mmax"
    new_times = trial_sections._get_event_section(
        data_with_sections, channel_name, section_times
    )
    assert len(new_times) == len_new_times


def test_extract_keyboard_section(data_with_sections):
    # Confirm length of original Sol data
    assert len(data_with_sections.Keyboard.times) == 68
    section_times = [0, 700]
    channel_name = "Keyboard"
    section_data = trial_sections._extract_keyboard_section(
        data_with_sections, channel_name, section_times
    )
    assert len(section_data.Keyboard.times) == 30
    assert len(section_data.Keyboard.codes) == 30


def test_extract_keyboard_section_value_error_message(data_with_sections, capsys):
    # Confirm length of original Sol data
    section_times = [0, 700]
    channel_name = "Stimcode"
    section_data = trial_sections._extract_keyboard_section(
        data_with_sections, channel_name, section_times
    )
    captured = capsys.readouterr()
    assert captured.out == "\t\tChannel Stimcode has no times and codes to extract.\n"


@pytest.mark.parametrize(
    "section_times, len_sol_times",
    [([1503, 1570], 132936), ([1207, 1289, 1503, 1570], 295635)],
)
def test_extract_section(data_with_sections, section_times, len_sol_times):
    assert len(data_with_sections.Sol.times) == 3776020
    section_data = trial_sections._extract_section(
        data_with_sections, "ramp", section_times
    )
    assert len(section_data.Sol.times) == len_sol_times


@pytest.mark.parametrize(
    "section_times, len_mmax_times",
    [([146, 254], 6), ([200, 254], 3)],
)
def test_extract_section_check_event(data_with_sections, section_times, len_mmax_times):
    assert len(data_with_sections.Mmax.times) == 14
    section_data = trial_sections._extract_section(
        data_with_sections, "mmax", section_times
    )
    assert len(section_data.Mmax.times) == len_mmax_times


# TODO: Add test for when stim channel present but does not have any `times`