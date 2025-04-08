# 1. TTS Preference Test Inteface 

## Overview
This repository provides code for preference test for speech synthesis experiments.


## Installation
### Prerequisites
Ensure you have the following dependencies installed:
- Python 3.x
- Required libraries: `gradio`, `argparse`, `glob`

### Usage

Run below code (prefarably in a tmux session) gives a shareable link to the evaluation interface.

```bash
python preference_test_code.py \
    --out_folder /home/hawau/Documents/projects/tts_evaluation/evaluation_results_experimentX \
    --sample_A /home/hawau/Documents/projects/evaluation/artst_arvoice_evaluation/wo_d \
    --sample_B /home/hawau/Documents/projects/evaluation/arvoice_h_r_wd_prolific
```

out_folder: individual preference scores per user will be saved in this folder

sample_A: this folder contains **.wav files** generated from experiment/model A

sample_B: this folder contains **.wav files** generated from experiment/model B

!!! 
- The number of samples in sample_A and sample_B must be equal.
- Ensure to include a control sample to validate the user's response.
- The code randomly shuffles the samples so displayed A contains samples from both experiments and vice versa. (Don't think too much about this, just so samples from experiment A are displayed as sample B sometimes to users)

### Usage With Prolific

Duplicate study `experiment_X` in drafts and edit details for your experiment.

Use the link generated from above as link to survey.

!!! The number of concurrent users **must be set to 1** to avoid response overwrite issues.
![alt text](image.png)



### Common Errors & Warnings

The error below occurs because gradio doesn't have access to paths, In line 153 of `preference_test_code.py` set `allowed_paths` to root path of audio samples.

```bash
...
raise InvalidPathError(msg)
gradio.exceptions.InvalidPathError: Cannot move ...
```

This warning can be ignored.
```bash
/home/hawau/miniconda3/envs/speech/lib/python3.10/site-packages/gradio/utils.py:999: UserWarning: Expected 1 arguments for function <function <lambda> at 0x7feb8592f6d0>, received 0.
  warnings.warn(
/home/hawau/miniconda3/envs/speech/lib/python3.10/site-packages/gradio/utils.py:1003: UserWarning: Expected at least 1 arguments for function <function <lambda> at 0x7feb8592f6d0>, received 0.
```
