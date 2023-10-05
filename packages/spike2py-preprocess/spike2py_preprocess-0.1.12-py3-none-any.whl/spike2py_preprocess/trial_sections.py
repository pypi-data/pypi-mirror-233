import copy
import sys

import numpy as np

import spike2py_preprocess.trial as trial


def extract(data, plot=False):
    section_names, section_times = _get_section_details(data)
    _validate_sections(section_names, data)
    section_name_times = _concat_section_names_times(section_names, section_times)
    for section_name, section_times in section_name_times.items():
        section_data = _extract_section(data, section_name, section_times)
        section_data = _rename_section_data(section_data, section_name)
        if plot:
            trial.plot_data(section_data)
        section_data.save()
        print(f"\t\tSaved {section_data.info.name}.pkl")


def _get_section_details(data):
    section_names = data.Memory.codes
    section_times = data.Memory.times
    return section_names, section_times


def _validate_sections(section_names, data):
    try:
        file_name = data.info.file.name
    except AttributeError:
        print(
            f"\t\tAll paths must be pathlib.Path objects, not strings."
            f"\n\t\tPlease correct for: {data.info.file}"
        )
        sys.exit(1)
    _even_number_of_sections(section_names, file_name)
    _matching_section_names(section_names, file_name)


def _concat_section_names_times(section_names: list, section_times: np.array) -> dict:
    """Group each unique section name and associated section times

    Parameters
    ----------
    section_names: Pairs of section names
                   e.g. ['mmax', 'mmax', 'threshold', 'threshold', 'mmax', 'mmax']
    section_times: Times associated with each name
                  e.g. array([ 146.55, 254.42, 796.43, 880.76, 1503.99, 1570.51])

    Returns
    -------
    Unique section names and all associated time pairs
    e.g. {'mmax': [146.55, 254.42, 1503.99, 1570.51],
          'threshold': [796.43, 880.76]
          }
    """
    unique_section_names = set(section_names)
    section_name_times = {section_name: [] for section_name in unique_section_names}
    for section_name, section_time in zip(section_names, section_times):
        section_name_times[section_name].append(section_time)
    return section_name_times


def _even_number_of_sections(section_names, file_name):
    if (len(section_names) % 2) != 0:
        message = (
            f"{file_name} has an uneven number of TextMarks on the Memory channel."
            " Please correct and rerun."
        )
        print(message)
        sys.exit(1)


def _matching_section_names(section_names, file_name):
    start = 0
    stop = int(len(section_names) / 2)
    step = 2
    for index in range(start, stop, step):
        section_name1 = section_names[index]
        section_name2 = section_names[index + 1]
        if section_name1 != section_name2:
            message = (
                f"\t\t{file_name} has pairs of TextMarks on the Memory channel that do not match."
                f"\n\t\t\tPlease correct and rerun."
            )
            print(message)
            sys.exit(1)


def _extract_section(data, section_name, section_times):
    channels = data.channels
    channels = _remove_memory_channel(channels)
    section_data = _extract_section_data(data, section_name, section_times, channels)
    return section_data


def _remove_memory_channel(channels):
    memory_channel_index = None
    for i, (channel_name, _) in enumerate(channels):
        if channel_name == "Memory":
            memory_channel_index = i
            break
    if memory_channel_index is not None:
        channels.pop(memory_channel_index)
    return channels


def _extract_waveform_section(section_data, channel_name, section_times):
    """For specified waveform channel, replace whole trial data with data from desired section

    Code extracts data for 'times', 'values', and 'raw_values' and then replaces the original data
    with extracted data.
    """
    time_indexes = _get_section_time_indexes(section_data, channel_name, section_times)

    new_times = _get_waveform_section_for(
        "times", section_data, channel_name, time_indexes
    )
    exec(f"section_data.{channel_name}.times = new_times")

    new_values = _get_waveform_section_for(
        "values", section_data, channel_name, time_indexes
    )
    exec(f"section_data.{channel_name}.values = new_values")

    new_raw_values = _get_waveform_section_for(
        "raw_values", section_data, channel_name, time_indexes
    )
    exec(f"section_data.{channel_name}.raw_values = new_raw_values")

    return section_data


def _get_waveform_section_for(channel_attr, section_data, channel_name, time_indexes):
    start = 0
    stop = int(len(time_indexes) / 2)
    step = 2
    new_data = list()
    for i in range(start, stop + 1, step):
        time1 = time_indexes[i]
        time2 = time_indexes[i + 1]
        exec(
            f"new_data.extend(list(section_data.{channel_name}.{channel_attr}[time1:time2]))"
        )
    return np.array(new_data)


def _get_section_time_indexes(section_data, channel_name, section_times):
    """Get the index of each pair of time points that identify data to keep"""
    channel_times = getattr(section_data, channel_name).times
    indexes = list()
    for time in section_times:
        index_current_time = find_nearest_time_index(channel_times, time)
        indexes.append(index_current_time)
    return indexes


def find_nearest_time_index(times, time):
    index = (np.abs(times - time)).argmin()
    return index


def _extract_event_section(section_data, channel_name, section_times):
    """For specified event channel, replace whole trial data with data from desired section"""
    if exec(f"len(section_data.{channel_name}.times)") != 0:
        new_times = _get_event_section(section_data, channel_name, section_times)
        exec(f"section_data.{channel_name}.times = new_times")
    return section_data


def _get_event_section(section_data, channel_name, section_times):
    start = 0
    stop = int(len(section_times) / 2)
    step = 2
    new_data = list()
    for i in range(start, stop + 1, step):
        time1 = section_times[i]
        time2 = section_times[i + 1]
        exec(
            f"current_times = np.vectorize(lambda time: {time1} <= time <= {time2})(section_data.{channel_name}.times)"
        )
        exec(f"new_data.extend(list(section_data.{channel_name}.times[current_times]))")
    return np.array(new_data)


def _extract_keyboard_section(section_data, channel_name, section_times):
    """For specified event channel, replace whole trial data with data from desired section"""
    try:
        new_times, new_codes = _get_keyboard_section(
            section_data, channel_name, section_times
        )
        exec(f"section_data.{channel_name}.times = np.array(new_times)")
        exec(f"section_data.{channel_name}.codes = new_codes")
    except ValueError:
        print(f"\t\tChannel {channel_name} has no times and codes to extract.")
    return section_data


def _get_keyboard_section(section_data, channel_name, section_times):
    start = 0
    stop = int(len(section_times) / 2)
    step = 2
    new_data_times = list()
    new_data_codes = list()
    for i in range(start, stop + 1, step):
        time1 = section_times[i]
        time2 = section_times[i + 1]
        exec(
            f"current_times = list(np.vectorize(lambda time: {time1} <= time <= {time2})(section_data.{channel_name}.times))"
        )
        exec(
            f"new_data_times.extend(list(section_data.{channel_name}.times[current_times]))"
        )
        exec(
            f"new_data_codes.extend(list(np.array(section_data.{channel_name}.codes)[current_times]))"
        )
    return new_data_times, new_data_codes


def _extract_section_data(data, section_name, section_times, channels):
    """Create deep copy of data and replace channel data with extracted section data

    Parameters
    ----------
    data: Instance of spike2py.trial.Trial containing all data from trial
    section_name: Name of section to extract data for
    section_times: Pairs of times (1 or more) marking data to extract
    channels: List of channels [(<channel_name>, <channel_type>), ...];
    e.g, [('Ds8', 'event'), ('Fdi', 'waveform')]


    """
    EXTRACT_SECTION_PER_CHANNEL_TYPE = {
        "waveform": _extract_waveform_section,
        "event": _extract_event_section,
        "keyboard": _extract_keyboard_section,
    }

    section_data = copy.deepcopy(data)
    for channel_name, channel_type in channels:
        channel = getattr(data, channel_name)
        if len(channel.times) > 0:
            section_data = EXTRACT_SECTION_PER_CHANNEL_TYPE[channel_type](
                section_data, channel_name, section_times
            )

    return section_data


def _rename_section_data(section_data, section_name):
    section_data.info.name = section_data.info.name + "_" + section_name
    return section_data
