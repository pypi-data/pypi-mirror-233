# fstlib - Python Library for Reading fst Files

## Introduction

`fstlib` is a Python library designed to facilitate the reading of fst (Fast Serialization of Data Frames) files using Python.  fst is specifically designed to unlock the potential of high speed solid state disks that can be found in most modern computers. Data frames stored in the fst format have full random access, both in column and rows.


## Features

- Read fst files in binary format
- Save fst files in binary format

## Installation

To start using `fstlib` to read and save FST (Fast Serialization of Data Frames) files in Python, follow these installation steps:

### Prerequisites

Before installing `fstlib`, ensure that you have the following prerequisites:

1. **Python**: Make sure Python is installed on your system. You can download Python from [python.org](https://www.python.org/downloads/) if you haven't already.

2. **`pip`**: Ensure that you have `pip`, the Python package manager, installed and up-to-date. You can upgrade `pip` using the following command:

```bash
   pip install --upgrade pip
   pip install git+https://github.com/finance-resilience/fstlib.git
```

3. **Aws credentials**: Since this package is private, it is usage is condition to the fact that you follow finres rules for
access_key document. So it will work only if you followed the rule we set in the organization.

Same, since the repository is private, pip may prompt you for your GitHub credentials. Please provide your GitHub username and a personal access token with appropriate repository access permissions when prompted.

Once the installation is complete, you can start using fstlib in your Python projects to work with FST files efficiently.

## Usage
Here's a simple example of how to use fstlib to read and save FST files:

```python
    from  fstlib import fstlib
    import os
    
    ##  read from AWS s3
    path_s3 = "projects/I4CE/402.MLEVA/SIM2/I4CE_SIM2_EVA_WING_GWL_15.fst"
    dteva = fstlib.fn_s3fdrd2(os.path.dirname(path_s3), 
                os.path.basename(path_s3))



    ## save locally fst
    fstlib.savefst(dteva, "~/Desktop/test.fst")

    # read locally fst
    dteva2 = fstlib.readfst("~/Desktop/testfunc.fst")
```

## Documentation

For more detailed information on how to use fstlib, please refer to the documentation (if available).

## License

This project is licensed under the MIT License.

## Contribution

Contributions of the team is welcome! If you encounter any issues or have suggestions for improvements, please feel free to open an issue or submit a pull request on the GitHub repository.