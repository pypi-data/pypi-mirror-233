[![spike2py](https://raw.githubusercontent.com/MartinHeroux/spike2py_preprocess/master/spike2py_preprocess_icon_600x300.png)](https://github.com/MartinHeroux/spike2py)


[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
    [![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-v2.0%20adopted-ff69b4.svg)](code_of_conduct.md)

**spike2py_preprocess** provides a simple way to batch (pre)process data with [spike2py](https://github.com/MartinHeroux/spike2py).

**spike2py_preprocess** can be used to batch read a series of `.mat` files and save them to `.pkl` files. 
However, the power of **spike2py_preprocess** is its ability to also preprocess the data, and this for a single trial, all trials from a subject, or all trials from a study.
Moreover, **spike2py_preprocess** can be used to extract only relevant sections of data; simply add two Spike2 TextMarks to mark the section of data to be extracted.
More than one section can be extracted per trial.

### Trial

In python:
```python
>>> from spike2py.trial import TrialInfo
>>> from spike2py_preprocess.trial import trial
>>> trial_info = TrialInfo(file="0004.mat",
                           name='h_reflex_curve',
                           subject_id='sub01',
                           path_save_trial='./proc')
>>> trial(trial_info)
```

On the command line:
```bash
$ python -m spike2py_preprocess trial --help
$ python -m spike2py_preprocess trial <path_to_trial_info_json>
```

or simply:

```bash
$ spike2py_preprocess trial --help
$ spike2py_preprocess trial <path_to_trial_info_json>
```

Here, we need to point `spike2py_preprocess.py` to a valid json file.
The json file requires the following fields:

```json
{
  "file": "/home/maple/study/sub01/data/raw/sub01_DATA000_H_B.mat",
  "channels": ["FDI", "W_EXT", "stim"],
  "name": "biphasic_high_fq",
  "subject_id": "sub01",
  "path_save_trial": "/home/maple/study/sub01/data/proc"
}
```

### Subject:

In Python:
```python
>>> from spike2py_preprocess.subject import subject
>>> from pathlib import Path
>>> subject_folder = Path('sub01')
>>> subject(subject_folder)
```
On the command line:
```bash
$ python -m spike2py_preprocess subject --help
$ python -m spike2py_preprocess subject /home/maple/study/sub01
```

or simply:
```bash
$ spike2py_preprocess subject --help
$ spike2py_preprocess subject /home/maple/study/sub01
```

### Study:

In Python: 

```python
>>> from spike2py_preprocess.study import study
>>> from pathlib import Path
>>> study_folder = Path('great_study')
>>> study(study_folder)
```

On the command line:
```bash
$ python -m spike2py_preprocess study --help
$ python -m spike2py_preprocess study /home/maple/study/
```

or simply:
```bash
$ spike2py_preprocess study --help
$ spike2py_preprocess study /home/maple/study/
```
## Preprocess

You can specify the preprocessing settings to apply to one or more channels by including one or more `<level>_preprocess.json` files.

For a single trial, **spike2py_preprocess** looks for `<trialname.mat>_preprocess.json` in the same folder as the `.mat` file.

For all trials for a subject, **spike2py_preprocess** looks for `subject_preprocess.json` in the provided subject folder.

Finally, for all trials in a study, **spike2py_preprocess** looks for `study_preprocess.json` in the provided study folder.

### Controlling the preprocessing

By including `study_preprocess.json`, `subject_preprocess.json` and `<trialname.mat>_preprocess.json` files in a given file structure, 
it is possible to provide a general preprocess scheme, but that can be overridden for a given subject or a given trial.

Below is an example of what could be included in a preprocess file. 
As you can see, each item is the name of a channel that exists in the `.mat` file. 

For each channel, a specific preprocessing step is specified.
At present, the preprocessing steps that are possible are those included in the `spike2py` 
[SignalProcessing](https://spike2py.readthedocs.io/en/latest/pages/reference_guides.html#sig-proc-signalprocessing)
mixin class.

The keys are the call to the preprocessing method, and the values are the inputs to those methods (if required).

```json
{
  "Fdi": {
    "remove_mean": "",
    "lowpass": "cutoff=200"
  },
  "W_Ext": {
    "remove_mean": "",
    "bandstop": "cutoff = [49, 51]"
  },
  "Stim": {
    "lowpass": "cutoff=20, order=8"
    }
}

```
#### IMPORTANT

Note that, in our example above, the channels were specified as `"channels": ["FDI", "W_EXT", "stim"]`,
but here they are specified as `Fdi`, `W_Ext`, and `Stim`. The reason for this is the researchers often used a wide
variety of styles to label channels, sometimes with ALLCAPS, other times with camel_case, or a combination of many.
To standardise things, `spike2py` applied TitleCase to each of the channel names.  If you are not 100% certain what the 
resulting channel name will be, simply apply `spike2py_preprocess` with you preprocess specified. This will result in a 
pickle (`.pkl`) file that can be opened with `spike2py`. 

```python
import spike2py as s2p
from pathlib import Path

tutorial = s2p.trial.load(file=Path('data.pkl'))
```

Now if you simply type `tutorial` and hit return, you will see information about the data, include the channel names.
## File structure

Below is an example of the required file/folder structure for **spike2py_preprocess**.

In the example, `sub02_DATA000_H_B.mat` has its own preprocess details located in **preprocess_sub02_DATA000_H_B.json**.

Similarly, at the subject level, `sub02` has a `subject_preprocess.json` file. This means all their files (excluding `sub02_DATA000_H_B.mat`) will be preprocessed in the same way.

Finally, because `sub01` does not include a dedicated `.json` file, their data would simply be read and saved as `.pkl` files if their data was analysed on their own. 
However, if **spike2py_preprocess** was used to preprocess all trials in the study, trials from `sub01` would be preprocessed with the details provided in `study_preprocess.json`.



### Study folder structure and required files

Below is an example study file structure. The study folder can have whatever name you like, `study1` in this case.
Similarly, the subject folders can have whatever names you like, but they should match the list of subjects you include
in the `study_info.json` file (see below for more details).

The raw data, in `.mat` format for each subject **must** be located in a folder with the name `raw`.

```bash

study1/
├── study_info.json
├── study_preprocess.json
├── sub01
│   ├── raw
│   │   ├── sub01_DATA000_H_B_trial_info.json
│   │   ├── sub01_DATA000_H_B.mat
│   │   ├── sub01_DATA001_C_B.mat
│   │   ├── sub01_DATA002_C_M.mat
│   │   └── sub01_DATA003_H_M.mat
│   └── subject_info.json
└── sub02
    ├── raw
    │   ├── preprocess_sub02_DATA000_H_B.json
    │   ├── sub02_DATA000_H_B.mat
    │   ├── sub02_DATA001_C_B.mat
    │   ├── sub02_DATA002_C_M.mat
    │   └── sub02_DATA003_H_M.mat
    ├── subject_info.json
    └── subject_preprocess.json
```

## subject_info.json
This file contains details about the subject. Additional information can appear in this file, but at a minimum it requires
that "subject_id" be provided, as well as "trials", which contains the various trials to be processed for this subject.
For each trial, the minimum data required is "name" and "file". If "channels" is provided, only these channels will be 
included and preprocessed; if not provided, all channels will be included.

```json
{
  "subject_id": "sub01",
  "age": 50,
  "gender": "F",
  "trials": {
    "trial1": {
      "name": "conv_biphasic",
      "file": "sub01_001.mat"
    },
    "trial2": {
      "name": "khz_biphasic",
      "file": "sub01_002.mat",
      "channels": ["FDI", "W_EXT", "stim"]
    }
  }
}

```
## study_info.json
This file contains details about the study. Additional information can appear in this file, but at a minimum it requires
that "name" and "subjects" be provided. If "channels" is provided, only these channels will be included and preprocessed,
noting that this can be trumped 
```json
{
    "name": "TSS_H-reflex",
    "subjects": [
      "sub01",
      "sub02"
    ],
  "channels": ["FDI", "W_EXT", "stim"]
}

```

## Spike2 TextMarks

Please refer to the document entitled "How_to_add_TextMarks_in_Spike2.pdf" for a guide on how to add TextMarks in Spike2.

If you add two TextMarks with the same label (e.g. 'MVC'), the section of data between the two TextMarks will be extracted and saved to a .pkl file.
Many such pairs of TextMarks can be included in a trial.

If you have two related sections of data, but want to exclude a middle section that is not useful or relevant,
you can add four labels, two around each section of data of interest, that have the same label, the data from both sections will be concatenated and extracted.

Note that Spike2 TextMarks need to be added prior to batch exporting the trial to .mat.

## Installing

**spike2py_preprocess** is available on PyPI:

```console
$ python -m pip install spike2py_preprocess
```

**spike2py** officially supports Python 3.8+.

## Contributing

Like this project? Want to help? We would love to have your contribution! Please see [CONTRIBUTING](CONTRIBUTING.md) to get started.

## Code of conduct

This project adheres to the Contributor Covenant code of conduct. By participating, you are expected to uphold this code. Please report unacceptable behavior to [heroux.martin@gmail.com](heroux.martin@gmail.com).

## License

[GPLv3](./LICENSE)
