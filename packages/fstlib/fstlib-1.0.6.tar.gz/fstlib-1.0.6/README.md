# fstlib - Python Library for Reading fst Files

## Introduction

`fstlib` is a Python library designed to facilitate the reading of fst (Fast Serialization of Data Frames) files using Python.  fst is specifically designed to unlock the potential of high speed solid state disks that can be found in most modern computers. Data frames stored in the fst format have full random access, both in column and rows. Click [here](https://www.fstpackage.org) to read more about the performances fst files compared to other tabular files.


## Features

- Read fst files in binary format
- Save fst files in binary format

## Installation

To start using `fstlib` to read and save FST (Fast Serialization of Data Frames) files in Python, follow these installation steps:

### Prerequisites

Before installing `fstlib`, ensure that you have the following prerequisites:

1. **Python**: Make sure Python is installed on your system. You can download Python from [python.org](https://www.python.org/downloads/) if you haven't already.

2. Install R langage in your computer from [CRAN](https://cran.r-project.org). If you don't have R in your laptop the installation will abort.

2. **`pip`**: Ensure that you have `pip`, the Python package manager, installed and up-to-date. You can upgrade `pip` using the following command:

```bash
   pip install --upgrade pip
   pip install git+https://github.com/finance-resilience/fstlib
```
or
```bash
   pip install --upgrade pip
   pip install fstlib
```

4. **Aws credentials**: Since this package is private, it is usage is condition to the fact that you follow finres rules for
access_key document. So it will work only if you followed the rule we set in the organization.

Same, since the repository is private, pip may prompt you for your GitHub credentials. Please provide your GitHub username and a personal access token with appropriate repository access permissions when prompted.

Once the installation is complete, you can start using fstlib in your Python projects to work with FST files efficiently.

## Usage
Here's a simple example of how to use fstlib to read and save FST files:

```python
    from  fstlib import fstlib
    import os
    import pandas as pd
    import numpy as np

    #path_s3 = "projects/I4CE/402.MLEVA/SIM2/I4CE_SIM2_EVA_WING_GWL_15.fst"
    
    # create a pandas dataframe
    df2 = pd.DataFrame(np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]]),columns=['a', 'b', 'c'])

    ## save the fst file
    fstlib.savefst(df2, "df2.fst")
    
    # read the fst file
    df = fstlib.readfst("df2.fst")
    
    df.shape

    os.remove("df2.fst")

```

## Documentation

For more detailed information on how to use fstlib, please refer to the documentation (if available).

## License

This project is licensed under the MIT License.

## Contribution

Contributions of the team is welcome! If you encounter any issues or have suggestions for improvements, please feel free to open an issue or submit a pull request on the GitHub repository.